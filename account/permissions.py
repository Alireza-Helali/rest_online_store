from rest_framework.permissions import BasePermission


class SuperUserPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            return user.is_superuser


class SignUpPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return True
        else:
            return False


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
