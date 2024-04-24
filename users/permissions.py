from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Class for checking if the user is the owner of the object."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsStaff(permissions.BasePermission):
    """Class for checking if the user is staff."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()
