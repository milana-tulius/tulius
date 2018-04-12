from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
                       url(r'^messages/$', PlayerMessagesView.as_view(), name='messages'),
                       url(r'^user/(?P<pk>\d+)/$', PlayerSendMessageView.as_view(), name='to_user'),
                       )
