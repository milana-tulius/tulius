import json

from django.db import models as dj_models

from tulius.forum.read_marks import models
from tulius.forum.comments import signals as comment_signals
from tulius.forum.threads import models as thread_models
from tulius.forum.threads import signals as thread_signals
from tulius.forum.threads import views
from tulius.forum.comments import models as comment_models
from tulius.forum.comments import views as comment_views
from tulius.forum.read_marks import tasks

# TODO game forum thread counters
# TODO update edge cases with changing threads (move)
# TODO test delete read mark


class ReadmarkAPI(views.BaseThreadView):
    require_user = True
    read_mark_model = models.ThreadReadMark
    comment_model = comment_models.Comment

    @classmethod
    def comment_json(cls, pk):
        comment = cls.comment_model.objects.get(id=pk) if pk else None
        return {
            'id': comment.pk,
            'thread': {
                'id': comment.parent_id,
            },
            'page': comment_views.order_to_page(comment.order),
        } if pk else None

    def mark_room_as_read(self, room):
        if room:
            threads = room.get_children(self.user, deleted=False)
        else:
            threads = self.thread_model.objects.filter(
                parent=None, deleted=False)
            threads = [t for t in threads if t.read_right(self.user)]
        for thread in threads:
            if thread.room:
                self.mark_room_as_read(thread)
            else:
                self.mark_thread_as_read(thread, None)
        if room:
            read_mark = self.read_mark_model.objects.filter(
                thread=room, user=self.user).first()
            if not read_mark:
                read_mark = self.read_mark_model(thread=room, user=self.user)
            read_mark.not_read_comment_id = None
            read_mark.save()

    def mark_parent_as_read(self, parent, child_read_mark):
        children = [
            t for t in parent.get_children(self.user)
            if t.pk != child_read_mark.thread.pk]
        read_marks = self.read_mark_model.objects.filter(
            user=self.user, thread__in=children)
        read_marks = {r.thread_id: r for r in read_marks}
        children = {c: read_marks.get(c.pk) for c in children}
        children[child_read_mark.thread] = child_read_mark
        parent_mark = self.read_mark_model.objects.filter(
            thread=parent, user=self.user).first()
        if not parent_mark:
            parent_mark = self.read_mark_model(thread=parent, user=self.user)
        old_not_read = parent_mark.not_read_comment_id
        parent_mark.not_read_comment_id = None
        for thread, read_mark in children.items():
            if read_mark:
                not_read_id = read_mark.not_read_comment_id
            else:
                not_read_id = thread.first_comment[self.user]
            if (parent_mark.not_read_comment_id is None) or (
                    not_read_id and (
                        parent_mark.not_read_comment_id > not_read_id)):
                parent_mark.not_read_comment_id = not_read_id
        if (old_not_read != parent_mark.not_read_comment_id) or \
                not parent_mark.pk:
            parent_mark.save()
            if parent.parent:
                self.mark_parent_as_read(parent.parent, parent_mark)

    def mark_thread_as_read(self, thread, read_id, with_parent=False):
        read_mark = self.read_mark_model.objects.filter(
            thread=thread, user=self.user).first()
        if not read_mark:
            read_mark = self.read_mark_model(thread=thread, user=self.user)
        if read_id:
            not_read = self.comment_model.objects.filter(
                parent=thread, id__gt=read_id, deleted=False
            ).exclude(user=self.user).order_by('id').first()
        else:
            not_read = None
        read_mark.not_read_comment_id = not_read.pk if not_read else None
        read_mark.save()
        if with_parent:
            self.mark_parent_as_read(thread.parent, read_mark)
        return read_mark

    @classmethod
    def not_read_comment_json(cls, comment_id, user):
        comment = cls.comment_model.objects.get(pk=comment_id)
        return {
            'id': comment.id,
            'page_num': comment_views.order_to_page(comment.order),
            'count': cls.comment_model.objects.filter(
                parent_id=comment.parent_id, deleted=False, id__gt=comment.id
            ).exclude(user=user).count() + 1
        }

    def post(self, *_args, **kwargs):
        if 'pk' in kwargs:
            self.get_parent_thread(**kwargs)
        read_id = json.loads(self.request.body)['comment_id']
        read_mark = None
        if (not self.obj) or self.obj.room:
            self.mark_room_as_read(self.obj)
        else:
            read_mark = self.mark_thread_as_read(
                self.obj, read_id, with_parent=True)
        return {
            'not_read': self.not_read_comment_json(
                read_mark.not_read_comment_id, self.user
            ) if read_mark and read_mark.not_read_comment_id else None
        }

    def delete(self, *_args, **kwargs):
        # TODO
        self.get_parent_thread(**kwargs)
        self.read_mark_model.objects.filter(
            thread=self.obj, user=self.user).delete()
        comment_id = self.obj.first_comment[self.user]
        return {
            'not_read':
                self.not_read_comment_json(
                    comment_id, self.user) if comment_id else None
        }

    @classmethod
    def on_delete_comment(cls, sender, comment, view, **_kwargs):
        thread = view.obj
        last_comment_id = thread.last_comment.su
        if (not comment.is_thread()) and (last_comment_id <= comment.pk):
            comments = sender.objects.filter(
                parent=thread, deleted=False, id__gt=comment.id).order_by('id')
            new_not_read = comments[0].id if comments else None
            count = cls.read_mark_model.objects.filter(
                thread=thread, not_read_comment_id=comment.pk
            ).update(not_read_comment_id=new_not_read)
            if count and thread.parent:
                tasks.update_read_marks_on_rights_async(thread.parent)

    @classmethod
    def after_add_comment(cls, comment, preview, view, **_kwargs):
        if preview:
            return
        if not comment.is_thread():
            pks = view.obj.parents_ids + [view.obj.pk]
            cls.read_mark_model.objects.filter(
                dj_models.Q(not_read_comment_id=None)
                | dj_models.Q(not_read_comment_id__gt=comment.pk),
                thread_id__in=pks,
            ).exclude(user=view.user).update(not_read_comment_id=comment.pk)

    @classmethod
    def update_response_with_marks(cls, response, user, threads):
        read_marks = {}
        if not user.is_anonymous:
            read_marks = cls.read_mark_model.objects.filter(
                thread__pk__in=threads.keys(), user=user)
            read_marks = {r.thread_id: r for r in read_marks}
        for thread_response in response:
            read_mark = read_marks.get(thread_response['id'])
            if not read_mark:
                pk = threads[thread_response['id']].first_comment[user]
                thread_response['not_read'] = cls.comment_json(pk)
            else:
                thread_response['not_read'] = \
                    cls.comment_json(read_mark.not_read_comment_id)

    @classmethod
    def on_prepare_room_list(cls, threads, view, response, **_kwargs):
        threads = {t.pk: t for t in threads}
        response['threads'].sort(
            key=lambda t: t.get('last_comment', {}).get('id', 0), reverse=True)
        cls.update_response_with_marks(
            response['rooms'] + response['threads'], view.user, threads)
        important = [t for t in response['threads'] if t['important']]
        not_read_threads = [
            t for t in response['threads']
            if (not t['important']) and t['not_read']]
        read_threads = [
            t for t in response['threads']
            if (not t['important']) and not t['not_read']]

        del response['threads'][:]
        response['threads'] += important + not_read_threads + read_threads

    @classmethod
    def on_index(cls, groups, response, view, **_kwargs):
        response_for_update = []
        threads = {}
        for group in groups:
            threads.update({room.pk: room for room in group.rooms})
        for group in response['groups']:
            response_for_update.extend(group['rooms'])
        cls.update_response_with_marks(response_for_update, view.user, threads)

        for group in response['groups']:
            not_read = None
            for room in group['rooms']:
                if room['not_read']:
                    if (not not_read) or (
                            room['not_read']['id'] < not_read['id']):
                        not_read = room['not_read']
            group['not_read'] = not_read

    @classmethod
    def on_thread_to_json(cls, instance, view, response, **_kwargs):
        not_read_comment = None
        if view.user.is_authenticated:
            readmark = cls.read_mark_model.objects.filter(
                thread=instance, user=view.user).first()
            if readmark:
                if readmark.not_read_comment_id:
                    not_read_comment = cls.not_read_comment_json(
                        readmark.not_read_comment_id, view.user)
            elif instance.first_comment[view.user]:
                not_read_comment = cls.not_read_comment_json(
                    instance.first_comment[view.user], view.user)
        response['not_read'] = not_read_comment


comment_signals.on_delete.connect(
    ReadmarkAPI.on_delete_comment, sender=comment_models.Comment)
comment_signals.after_add.connect(
    ReadmarkAPI.after_add_comment, sender=comment_models.Comment)
thread_signals.prepare_room.connect(
    ReadmarkAPI.on_prepare_room_list, sender=thread_models.Thread)
thread_signals.to_json.connect(
    ReadmarkAPI.on_thread_to_json, sender=thread_models.Thread)
thread_signals.index_to_json.connect(
    ReadmarkAPI.on_index, sender=thread_models.Thread)
