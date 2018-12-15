from django.conf.urls import url, include
from euclid_authorization import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^account/$', views.CurrentClient.as_view(), name='client'),
    url(r'^account/', include('rest_framework.urls')),
    url(r'^account/register/$', views.ClientRegistration.as_view(), name='client-registration'),
    url(r'^account/password/change/$', views.ClientPasswordChange.as_view(), name='client-password-change'),
    url(r'^account/device/add', views.FCMDeviceCreate.as_view(), name='client-device-add'),
    url(r'^token/authorize/', obtain_jwt_token, name='token-auth'),
]