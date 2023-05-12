from rest_framework import permissions


class OwnerAuthenticatedOrReadOnlyPermission(permissions.BasePermission):
    UNSAFE_METHODS = ("POST", "PUT", "PATCH", "DELETE")

    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        elif request.method in self.UNSAFE_METHODS and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        elif request.method in self.UNSAFE_METHODS and request.user.is_authenticated:
            return request.user == obj.created_by
        return False
