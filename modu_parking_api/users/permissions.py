from rest_framework import permissions


class CustomUserPermission(permissions.BasePermission):
    """
    Custom permission to only allow anyone to (get, create) objects
    and only owners of an object to (update, delete) it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True
        return obj == request.user
