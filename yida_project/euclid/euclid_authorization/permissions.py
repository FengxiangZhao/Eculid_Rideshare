from rest_framework import permissions

class IsAnonymousOrReadOnly(permissions.BasePermission):
    '''
    Allow access only if the request.user is unregistered (anonymous)
    Used in the registration stage to prevent illegal access
    '''
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or not request.user.is_authenticated:
            return True
        return False