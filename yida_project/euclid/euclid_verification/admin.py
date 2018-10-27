from django.contrib import admin

from .models import EmailVerificationToken

class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'client', 'created_time')
    ordering = ('-created_time',)
    readonly_fields = ('client', 'token')

    def has_add_permission(self, request):
        '''
        Reject all adding from user
        '''
        return False

admin.site.register(EmailVerificationToken, EmailVerificationTokenAdmin)
