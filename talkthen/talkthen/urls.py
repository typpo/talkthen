from django.conf.urls import patterns, include, url
from django.contrib import admin

from core.models import PhoneNumber, Call

admin.autodiscover()

admin.site.register(PhoneNumber)
admin.site.register(Call)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'talkthen.views.home', name='home'),
    url(r'^api/', include('api.urls')),
    url(r'^core/', include('core.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('web.urls')),
)
