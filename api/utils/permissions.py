from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsNotAuthenticated(BasePermission):
    message = 'You are should be not Authenticated'

    def has_permission(self, request, view):
        return bool(not request.user.is_authenticated)


class CheckUserPermissionToGetMovieLink(BasePermission):
    message = "You don't have permission to get movie link"

    def has_object_permission(self, request, view, obj):
        if obj.is_free:
            return True
        if not request.user.is_authenticated:
            return False
        return bool(request.user.has_plan())


class ProfilePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj or request.user.is_staff)
