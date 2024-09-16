from rest_framework.permissions import BasePermission


class IsOstad(BasePermission):
    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                getattr(request.user.profile, 'user_type', None) == 'ostad'
        )


class AllowGETForAnonymous(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user and request.user.is_authenticated
