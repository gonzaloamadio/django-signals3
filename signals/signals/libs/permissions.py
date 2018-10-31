from rest_framework import permissions

class RelatedUserOnly(permissions.BasePermission):
    """
    Full rights granted only to related user
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class SameUserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user
