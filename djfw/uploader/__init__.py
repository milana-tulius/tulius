import json
from wsgiref import util

from django import http
from django.core.files import base


def handle_upload(request, func, *args, **kwargs):
    """
    Uploading files via Ajax
    """
    if request.method == "POST":
        if not request.FILES:
            upload = base.ContentFile(request.read())
            if 'qqfile' in request.GET:
                filename = request.GET['qqfile']
            else:
                filename = ""
        else:
            if len(request.FILES) == 1:
                upload = next(request.FILES.values())
            else:
                raise http.Http404('Bad Upload')
            filename = upload.name
    res = func(request, upload, filename, *args, **kwargs)
    # let Ajax Upload know whether we saved it or not
    ret_json = {'success': True}
    if res:
        ret_json = res
        res['success'] = True
    return http.HttpResponse(json.dumps(ret_json))


def handle_field_upload(request, field, target_filename):
    def save(request, upload, filename, field, target_filename):
        if field.name != '':
            field.delete()
        field.save(target_filename, upload)

    return handle_upload(request, save, field, target_filename)


def handle_download(file_obj, file_name, mime_type=''):
    if mime_type:
        response = http.HttpResponse(file_obj, mimetype='image')
    else:
        response = http.HttpResponse(file_obj)
    response['Content-Disposition'] = 'filename=' + file_name
    return response


def handle_download_file_path(file_path, file_name, mime_type=''):
    file_obj = util.FileWrapper(open(file_path, "rb"))
    return handle_download(file_obj, file_name, mime_type)


def handle_field_download(field, file_name, mime_type=''):
    field.open()
    return handle_download(field, file_name, mime_type)
