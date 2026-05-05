from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Разрешение для владельца объекта.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsPublic(BasePermission):
    """
    Разрешение для просмотра публичных привычек.
    """
    def has_object_permission(self, request, view, obj):
        return obj.is_public