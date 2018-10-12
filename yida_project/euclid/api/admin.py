from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin


from .models import Client

admin.site.register(Client, UserAdmin)
admin.site.unregister(Group)
