from django.conf.urls import url, include
from api import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^account/$', views.CurrentClient.as_view(), name='client'),
    url(r'^account/', include('rest_framework.urls')),
    url(r'^account/register/$', views.ClientRegistration.as_view(), name='client-registration'),
    url(r'^token/authorize/', obtain_jwt_token, name='token-auth'),
    url(r'^token/refresh/', refresh_jwt_token, name='token-refresh'),
]

urlpatterns += [
    url(r'^driver/$', views.DriverScheduleList.as_view(), name='driver-schedule-list'),
    url(r'^driver/(?P<pk>[0-9]+)/$', views.DriverScheduleDetail.as_view(), name='driver-schedule-detail'),
    url(r'^rider/$', views.RiderScheduleList.as_view(), name='rider-schedule-list'),
    url(r'^rider/(?P<pk>[0-9]+)/$', views.RiderScheduleDetail.as_view(), name='rider-schedule-detail'),
]
