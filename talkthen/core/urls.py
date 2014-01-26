from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^call_placed/(?P<call_pk>\d+)/$', 'core.views.call_placed', name='call_placed'),
    url(r'^sms_received/$', 'core.views.sms_received', name='sms_received'),
)
