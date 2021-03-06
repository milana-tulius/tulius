from unittest import mock
from django import http

from tulius.forum import core


class FooView(core.BaseAPIView):
    def get_context_data(self, **kwargs):
        return http.HttpResponseRedirect('/foobar')


def test_api_can_return_django_response():
    view = FooView.as_view()
    response = view(mock.Mock(method='GET'))
    assert response.status_code == 302
