from django.conf.urls import patterns, include, url
from rest_framework import viewsets, routers

from api import views

router = routers.DefaultRouter()
router.register(r'phone_numbers', views.PhoneNumberViewSet)
router.register(r'calls', views.CallViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
