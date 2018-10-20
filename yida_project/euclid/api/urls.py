from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^driver/$', views.DriverScheduleList.as_view(), name='driver-schedule-list'),
    url(r'^driver/(?P<pk>[0-9]+)/$', views.DriverScheduleDetail.as_view(), name='driver-schedule-detail'),
    url(r'^rider/$', views.RiderScheduleList.as_view(), name='rider-schedule-list'),
    url(r'^rider/(?P<pk>[0-9]+)/$', views.RiderScheduleDetail.as_view(), name='rider-schedule-detail'),
    url(r'^client/$', views.ClientList.as_view(), name='client-list'),
    url(r'^client/(?P<pk>[0-9]+)/$', views.ClientDetail.as_view(), name='client-detail'),
    url(r'^registration/$', views.ClientRegistration.as_view(), name='client-registration')
]