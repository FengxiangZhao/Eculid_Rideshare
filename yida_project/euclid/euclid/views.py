from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
@permission_classes((permissions.AllowAny,)) # Allow any to view the API root
def api_root(request, format=None):
    '''
    provide an entry point for the API Views in the form of http links
    '''
    return Response({
        'Client Information': reverse('client', request=request, format=format),
        'Client Registration': reverse('client-registration', request=request, format=format),
        'Client Password Change' : reverse('client-password-change', request=request, format=format),
        'Client Token Authorization' : reverse('token-auth', request=request, format=format),
        'Client Token Refresh' : reverse('token-refresh', request=request, format=format),
        'Driver Schedule': reverse('driver-schedule-list', request=request, format=format),
        'Rider Schedule' : reverse('rider-schedule-list', request=request, format=format)
    })
