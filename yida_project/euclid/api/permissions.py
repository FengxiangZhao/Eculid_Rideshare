from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    '''
    Allow object access only if the request.user is the owner of the object
    '''
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsVerifiedUserOrReadOnly(permissions.BasePermission):
    '''
    Allow access only if the request.user has the email verified
    '''
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or (request.user.is_authenticated and request.user.is_email_verified):
            return True
        return False

class IsAnonymousOrReadOnly(permissions.BasePermission):
    '''
    Allow access only if the request.user is unregistered (anonymous)
    Used in the registration stage to prevent illegal access
    '''
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or not request.user.is_authenticated:
            return True
        return False