from rest_framework import permissions

from .models import UserRoleChoices


class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == UserRoleChoices.ADMIN
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and request.user.role == UserRoleChoices.ADMIN
        )


class IsAdminOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role >= UserRoleChoices.MANAGER
        )


class IsAdminOrOwnerOrManagerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and request.user.role >= UserRoleChoices.MANAGER
            or request.user == obj.creator
        )
