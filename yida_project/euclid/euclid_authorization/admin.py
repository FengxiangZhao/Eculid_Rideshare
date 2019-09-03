from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from .models import Client
from .verifications import validate_case_email

class ClientCreationForm(forms.ModelForm):
    """
    A form for creating new user
    """
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Client
        fields = ('username', 'pwd', 'email', 'phone')

    def save(self, commit=True):
        # Save the provided password in hashed format
        client = super(ClientCreationForm, self).save(commit=False)
        client.set_password(self.cleaned_data["password"])
        if commit:
            client.save()
        return client

    def clean_email(self, email):
        if not validate_case_email(email):
            raise forms.ValidationError("The email address provided is not a valid CWRU email address.")
        return email


class ClientAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = ClientCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('pwd',)}),
        ('Permissions', {'fields': ('is_superuser',)}),
        # ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'pwd', 'email', 'password')}
         ),
    )
    search_fields = ('username', 'email',)
    ordering = ('username', 'email',)
    filter_horizontal = ()

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(UserAdmin, self).get_readonly_fields(request, obj)
        if obj: # editing an existing object
            return readonly_fields + ['email']
        return readonly_fields



admin.site.register(Client, ClientAdmin)
admin.site.unregister(Group)

