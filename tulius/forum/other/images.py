import io

from django import dispatch
from django.core import exceptions
from django.core.files import uploadedfile

from tulius.forum import core
from tulius.forum.threads import signals as thread_signals
from tulius.forum.comments import signals as comment_signals
from djfw.wysibb import models
from djfw.wysibb import views as djfw_views


def validate_image_data(images_data):
    result = []
    for image_data in images_data:
        image = models.UploadedImage.objects.get(id=image_data['id'])
        result.append(Images.image_to_json(image))
    return result


@dispatch.receiver(thread_signals.before_create)
def before_create_thread(instance, data, **_kwargs):
    if instance.room:
        return
    images_data = data['media'].get('images')
    if not images_data:
        return
    instance.media['images'] = validate_image_data(images_data)


@dispatch.receiver(comment_signals.before_add)
def before_add_comment(comment, data, view, **_kwargs):
    images_data = data['media'].get('images')
    if not images_data:
        return
    if comment.is_thread():
        comment.media['images'] = view.obj.media['images']
    else:
        comment.media['images'] = validate_image_data(images_data)


@dispatch.receiver(comment_signals.on_update)
def on_comment_update(comment, data, view, **_kwargs):
    images_data = data['media'].get('images')
    orig_data = comment.media.get('images')
    if images_data:
        images_data = validate_image_data(images_data)
    if orig_data and not images_data:
        del comment.media['images']
    elif images_data:
        comment.media['images'] = images_data
    if comment.is_thread():
        if (not images_data) and ('images' in view.obj.media):
            del view.obj.media['images']
        elif images_data:
            view.obj.media['images'] = images_data


class Images(core.BaseAPIView):
    require_user = False

    @staticmethod
    def image_to_json(image):
        return {
            'id': image.id,
            'file_name': image.filename,
            'url': image.image.url if image.image else None,
            'thumb': image.thumb.url if image.thumb else None,
        }

    def get_context_data(self, **kwargs):
        images = models.UploadedImage.objects.filter(
            user=self.user).order_by('-id')[:50]
        return {'images': [
            self.image_to_json(image) for image in images
        ]}

    @staticmethod
    def put(request):
        if not request.user.is_authenticated:
            raise exceptions.PermissionDenied()
        uploaded = uploadedfile.InMemoryUploadedFile(
            io.BytesIO(request.body),
            'upload',
            request.GET['file_name'],
            content_type=request.GET['content_type'],
            size=len(request.body),
            charset=None
        )
        response = djfw_views.save_uploaded_image(
            request, uploaded, request.GET['file_name'])
        return {
            'id': response['id'],
            'file_name': response['file_name'],
            'url': response['image_link'],
            'thumb': response['thumb_link'],
        }
