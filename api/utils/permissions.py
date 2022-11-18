from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsNotAuthenticated(BasePermission):
    message = 'You are should be not Authenticated'

    def has_permission(self, request, view):
        return bool(not request.user.is_authenticated)
