import json

from django import dispatch
from django import http
from django import shortcuts
from django import urls
from django.core import exceptions
from django.core.cache import cache
from django.utils import html
from django.db import transaction
from django.db.models import query_utils

from tulius.core.ckeditor import html_converter
from tulius.forum import core
from tulius.forum import const
from tulius.forum import rights as forum_rights
from tulius.forum import online_status as online_status_plugin
from tulius.forum.threads import models
from tulius.forum.threads import signals
from tulius.forum.rights import models as rights_models
from djfw.wysibb.templatetags import bbcodes


def user_to_json(user, detailed=False):
    data = {
        'id': user.id,
        'title': html.escape(user.username),
        'url': user.get_absolute_url(),
    }
    if detailed:
        if user.show_online_status:
            online_status = online_status_plugin.get_user_status(user.id)
        else:
            online_status = False
        data.update({
            'sex': user.sex,
            'avatar': user.avatar.url if user.avatar else '',
            'full_stars': user.full_stars(),  # TODO optimize it
            'rank': html.escape(user.rank),
            'stories_author': user.stories_author,
            'signature': bbcodes.bbcode(user.signature),
            'online_status': bool(online_status)
        })
    return data


class BaseThreadView(core.BaseAPIView):
    obj = None
    rights = None
    thread_model = models.Thread

    def _get_rights_checker(self, thread, parent_rights=None):
        return forum_rights.default.DefaultRightsChecker(
            thread, self.user, parent_rights=parent_rights)

    def get_parent_thread(self, pk=None, for_update=False, **kwargs):
        thread_id = int(pk)
        query = self.thread_model.objects.filter(deleted=False)
        if for_update:
            query = query.select_for_update()
        self.obj = shortcuts.get_object_or_404(query, id=thread_id)
        # TODO delete all sub threads and rooms on room delete so it will be
        # TODO not needed to do parent check here
        if self.obj.check_deleted():
            raise http.Http404('Post was deleted')
        self.rights = self._get_rights_checker(self.obj).get_rights()
        if not self.rights.read:
            raise exceptions.PermissionDenied()

    def _thread_list_apply_rights(self, parent_rights, thread_list):
        for thread in thread_list:
            thread.rights_checker = self._get_rights_checker(
                thread, parent_rights=parent_rights)
            thread.rights = thread.rights_checker.get_rights()
        return [thread for thread in thread_list if thread.rights.read]

    @staticmethod
    def room_descendants(room):
        if room.rght - room.lft <= 1:
            return [], []
        readable = room.rights_checker.get_readable_descendants()
        room_list = [thread for thread in readable if thread.room]
        threads = [thread for thread in readable if not thread.room]
        new_room_list = []
        # TODO remove: looks like all this magic is needed just for case
        # TODO of filtering children of deleted rooms
        while room_list:
            tested_room = room_list.pop(0)
            parent_id = tested_room.parent_id
            found_parent = (parent_id == room.id)
            if not found_parent:
                for tmp in room_list:
                    if tmp.id == parent_id:
                        found_parent = True
                        break
            if not found_parent:
                for tmp in new_room_list:
                    if tmp.id == parent_id:
                        found_parent = True
                        break
            if not found_parent:
                lft = tested_room.lft
                rght = tested_room.rght
                room_list = [
                    tmp for tmp in room_list if
                    not ((tmp.lft > lft) and (tmp.rght < rght))]
                new_room_list = [
                    tmp for tmp in new_room_list if
                    not ((tmp.lft > lft) and (tmp.rght < rght))]
            else:
                new_room_list += [tested_room]
        room_ids = [tmp.id for tmp in new_room_list]
        threads = [
            thread for thread in threads if
            (thread.parent_id == room.id) or (thread.parent_id in room_ids)]
        return new_room_list, threads

    def prepare_room_list(self, parent_rights, rooms):
        rooms = self._thread_list_apply_rights(parent_rights, rooms)
        for room in rooms:
            threads = self.room_descendants(room)[1]
            threads = self._thread_list_apply_rights(room.rights, threads)
            room.threads_count = len(threads)
            room.moderators, room.accessed_users = room.rights_checker\
                .get_moderators_and_accessed_users()
            signals.prepare_room.send(
                self.thread_model, room=room, threads=threads, view=self)
        return rooms

    def get_subthreads(self, is_room=False):
        threads = self.thread_model.objects.filter(
            parent=self.obj, room=is_room).exclude(deleted=True)
        if is_room:
            return self.prepare_room_list(self.rights, threads)
        threads = threads.order_by('-last_comment_id')
        threads = self._thread_list_apply_rights(self.rights, threads)

        for thread in threads:
            thread.moderators, thread.accessed_users = thread.rights_checker\
                    .get_moderators_and_accessed_users()
        signals.prepare_threads.send(
            self.thread_model, threads=threads, view=self)
        return threads

    @staticmethod
    def thread_url(thread_id):
        return urls.reverse('forum_api:thread', kwargs={'pk': thread_id})

    def room_to_json(self, thread):
        data = {
            'id': thread.pk,
            'title': html.escape(thread.title),
            'body': bbcodes.bbcode(thread.body),
            'room': thread.room,
            'deleted': thread.deleted,
            'important': thread.important,
            'closed': thread.closed,
            'user': user_to_json(thread.user),
            'moderators': [user_to_json(user) for user in thread.moderators],
            'accessed_users': None if thread.accessed_users is None else [
                user_to_json(user) for user in thread.accessed_users
            ],
            'threads_count': thread.threads_count if thread.room else None,
            'url': self.thread_url(thread.pk),
        }
        signals.room_to_json.send(
            self.thread_model, instance=thread, response=data, view=self)
        return data

    def create_thread(self, data):
        room = bool(data['room'])
        important = ((not room) and data.get('important', False))
        return self.thread_model(
            parent=self.obj, room=room,
            title=data['title'], body=data['body'],
            user=self.user,
            important=self.rights.moderate and important,
        )

    def update_thread(self, data):
        self.obj.title = data['title']
        self.obj.body = data['body']
        if self.rights.moderate and not self.obj.room:
            self.obj.important = bool(data['important'])
            self.obj.closed = bool(data['closed'])

    def obj_to_json(self):
        data = {
            'id': self.obj.pk,
            'tree_id': self.obj.tree_id,
            'title': self.obj.title,
            'body': bbcodes.bbcode(self.obj.body),
            'room': self.obj.room,
            'deleted': self.obj.deleted,
            'url': self.thread_url(self.obj.pk) if self.obj.pk else None,
            'parents': [{
                'id': parent.id,
                'title': parent.title,
                'url': self.thread_url(parent.pk),
            } for parent in self.obj.get_ancestors()] if self.obj.pk else None,
            'rights': self.rights.to_json(),
            'access_type': self.obj.access_type,
            'first_comment_id': self.obj.first_comment_id,
        }
        if self.obj.room:
            data['rooms'] = [
                self.room_to_json(t) for t in self.get_subthreads(True)]
            data['threads'] = [
                self.room_to_json(t) for t in self.get_subthreads(False)]
        else:
            data['closed'] = self.obj.closed
            data['important'] = self.obj.important
            data['user'] = user_to_json(self.obj.user, detailed=True)
            data['media'] = self.obj.media
        return data

    @classmethod
    def on_fix_counters(cls, sender, thread, view, **kwargs):
        sender.objects.partial_rebuild(thread.tree_id)


dispatch.receiver(signals.on_fix_counters)(BaseThreadView.on_fix_counters)


class ThreadView(BaseThreadView):
    delete_mark_model = models.ThreadDeleteMark

    def get_context_data(self, **kwargs):
        super(ThreadView, self).get_context_data(**kwargs)
        if self.obj is None:
            self.get_parent_thread(**kwargs)
        # cache rights for async app
        cache.set(
            const.USER_THREAD_RIGHTS.format(
                user_id=self.user.id, thread_id=self.obj.pk),
            'r', const.USER_THREAD_RIGHTS_PERIOD * 60
        )
        response = self.obj_to_json()
        signals.to_json.send(
            self.thread_model, instance=self.obj, response=response, view=self)
        return response

    @transaction.atomic
    def delete(self, request, **kwargs):
        self.get_parent_thread(for_update=True, **kwargs)
        if not self.rights.edit:
            raise exceptions.PermissionDenied()
        self.obj.deleted = True
        delete_mark = self.delete_mark_model(
            thread=self.obj,
            user=self.user,
            description=request.GET['comment'])
        self.obj.save()
        delete_mark.save()
        return {'result': True}

    def put(self, request, **kwargs):
        data = json.loads(request.body)
        data['title'] = html_converter.html_to_bb(data['title'])
        data['body'] = html_converter.html_to_bb(data['body'])
        preview = data.pop('preview', False)
        transaction.set_autocommit(False)
        self.get_parent_thread(for_update=not preview, **kwargs)
        if not self.rights.write:
            raise exceptions.PermissionDenied()
        self.obj = self.create_thread(data)
        signals.before_create.send(
            self.thread_model, instance=self.obj, data=data, view=self)
        if not preview:
            self.obj.save()
        signals.after_create.send(
            self.thread_model, instance=self.obj, data=data, preview=preview,
            view=self)
        transaction.commit()
        # TODO notify clients
        response = self.obj_to_json()
        signals.to_json.send(
            self.thread_model, instance=self.obj, response=response, view=self)
        return response

    @transaction.atomic
    def post(self, request, **kwargs):
        data = json.loads(request.body)
        data['title'] = html_converter.html_to_bb(data['title'])
        data['body'] = html_converter.html_to_bb(data['body'])
        preview = data.pop('preview', False)
        self.get_parent_thread(for_update=True, **kwargs)
        if not self.rights.edit:
            raise exceptions.PermissionDenied()
        self.update_thread(data)
        signals.on_update.send(
            self.thread_model, instance=self.obj, data=data, preview=preview,
            view=self)
        if not preview:
            self.obj.save()
        response = self.obj_to_json()
        signals.to_json.send(
            self.thread_model, instance=self.obj, response=response, view=self)
        return response


class IndexView(BaseThreadView):
    rights_model = rights_models.ThreadAccessRight

    def get_index(self, level):
        children = list(self.get_free_index(level)) + \
            list(self.get_readable_protected_index(level))
        children = [thread for thread in children if thread.room]
        return sorted(children, key=lambda x: x.id)

    def get_readable_protected_index(self, level):
        if self.user.is_superuser:
            return self.thread_model.objects.filter(
                access_type=models.THREAD_ACCESS_TYPE_NO_READ,
                level=level, deleted=False)
        if self.user.is_anonymous:
            return []
        query = query_utils.Q(
            thread__level=level,
            thread__access_type=models.THREAD_ACCESS_TYPE_NO_READ,
            access_level__gte=rights_models.THREAD_ACCESS_READ,
            user=self.user, thread__deleted=False)
        rights = self.rights_model.objects.filter(query)
        rights = rights.select_related('thread')
        return [right.thread for right in rights]

    def get_free_index(self, level):
        threads = self.thread_model.objects.filter(
            access_type__lt=models.THREAD_ACCESS_TYPE_NO_READ,
            level=level, deleted=False)
        if self.user.is_anonymous:
            return threads
        return threads.filter(query_utils.Q(
            access_type__lt=models.THREAD_ACCESS_TYPE_NO_READ
        ) | query_utils.Q(user=self.user))  # TODO: move it to protected #97

    def room_group_unreaded(self, rooms):
        unreaded = None
        for room in rooms:
            if room.unreaded:
                if (not unreaded) or (room.unreaded_id < unreaded.id):
                    unreaded = room.unreaded
        return {
            'id': unreaded.id,
            'thread': {
                'id': unreaded.parent_id,
                'url': self.thread_url(unreaded.parent_id),
            },
            'page': unreaded.page
        } if unreaded else None

    def get_context_data(self, **kwargs):
        all_rooms = list(self.get_index(1))
        groups = self.get_index(0)
        self.rights = self._get_rights_checker(None).get_rights_for_root()
        for group in groups:
            group.rooms = [
                thread for thread in all_rooms if thread.parent_id == group.id]
            for thread in group.rooms:
                thread.parent = group
            group.rooms = self.prepare_room_list(self.rights, group.rooms)
            # TODO refactor unread url, move it to readmarks
        return {
            'groups': [{
                'id': group.id,
                'title': group.title,
                'rooms': [self.room_to_json(thread) for thread in group.rooms],
                'url': self.thread_url(group.id),
                'unreaded': self.room_group_unreaded(group.rooms),
            } for group in groups]
        }

    def put(self, request, **_kwargs):
        transaction.set_autocommit(False)
        self.rights = self._get_rights_checker(None).get_rights_for_root()
        if not self.rights.moderate:
            raise exceptions.PermissionDenied()
        data = json.loads(request.body)
        data['title'] = html_converter.html_to_bb(data['title'])
        data['body'] = html_converter.html_to_bb(data['body'])
        if not data['room']:
            raise exceptions.PermissionDenied()
        thread = self.create_thread(data)
        signals.before_create.send(
            self.thread_model, instance=thread, data=data, view=self)
        thread.save()
        signals.after_create.send(
            self.thread_model, instance=thread, data=data, preview=False,
            view=self)
        transaction.commit()
        # TODO notify clients
        return {'id': thread.pk, 'url': self.thread_url(thread.pk)}


class MoveThreadView(BaseThreadView):
    @transaction.atomic
    def put(self, request, **kwargs):
        data = json.loads(request.body)
        parent_id = data['parent_id']
        self.get_parent_thread(parent_id, for_update=True)
        if not self.rights.write:
            raise exceptions.PermissionDenied('No target write right')
        new_parent = self.obj
        self.get_parent_thread(for_update=True, **kwargs)
        if not self.rights.edit:
            raise exceptions.PermissionDenied('No source edit right')
        if new_parent.is_descendant_of(self.obj, include_self=True):
            raise exceptions.PermissionDenied('Cant move inside yourself')
        old_parent = self.obj.parent
        self.obj.parent = new_parent
        self.obj.save()
        if old_parent and ((not new_parent) or (
                old_parent.tree_id != new_parent.tree_id)):
            obj = self.thread_model.objects.get(
                tree_id=old_parent.tree_id, parent=None)
            self.on_fix_counters(self.thread_model, obj, self)
            obj.save()
        if new_parent:
            obj = self.thread_model.objects.get(
                tree_id=new_parent.tree_id, parent=None)
            self.on_fix_counters(self.thread_model, obj, self)
            obj.save()
        response = self.obj_to_json()
        signals.to_json.send(
            self.thread_model, instance=self.obj, response=response, view=self)
        return response
