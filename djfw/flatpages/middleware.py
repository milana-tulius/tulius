from django import http
from django.conf import settings

from djfw.flatpages import views


class FlatpageFallbackMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code != 404:
            # No need to check for a flatpage for non-404 responses.
            return response
        try:
            return views.flatpage(request, request.path_info)
        # Return the original response if any errors happened. Because this
        # is a middleware, we can't assume the errors will be caught elsewhere.
        except http.Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response
