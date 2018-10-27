from django.conf.urls import url, include
from euclid_userauth import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    url(r'^account/$', views.CurrentClient.as_view(), name='client'),
    url(r'^account/', include('rest_framework.urls')),
    url(r'^account/register/$', views.ClientRegistration.as_view(), name='client-registration'),
    url(r'^token/authorize/', obtain_jwt_token, name='token-auth'),
    url(r'^token/refresh/', refresh_jwt_token, name='token-refresh'),
]