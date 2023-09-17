from rest_framework import permissions
from .models import CustomUser


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admins to access.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and
            request.user.role == CustomUser.ADMIN)
