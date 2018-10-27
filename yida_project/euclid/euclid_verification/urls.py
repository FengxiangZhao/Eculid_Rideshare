from django.conf.urls import url
from euclid_verification import views

urlpatterns = [
    url(r'^email/verify/$', views.client_email_verify),
    url(r'^email/reset/$', views.client_email_reset),
]