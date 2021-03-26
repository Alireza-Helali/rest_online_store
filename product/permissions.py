from rest_framework.permissions import BasePermission


class TagPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and user.is_supplier:
            return True
