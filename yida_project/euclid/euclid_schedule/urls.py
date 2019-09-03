from django.conf.urls import url, include
from euclid_schedule import views


urlpatterns = [
    url(r'^driver/$', views.DriverScheduleList.as_view(), name='driver-schedule-list'),
    url(r'^driver/(?P<pk>[0-9]+)/$', views.DriverScheduleDetail.as_view(), name='driver-schedule-detail'),
    url(r'^rider/$', views.RiderScheduleList.as_view(), name='rider-schedule-list'),
    url(r'^rider/(?P<pk>[0-9]+)/$', views.RiderScheduleDetail.as_view(), name='rider-schedule-detail'),
]
