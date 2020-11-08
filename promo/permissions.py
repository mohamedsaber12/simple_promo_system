from rest_framework.permissions import BasePermission


class IsAdministration(BasePermission):
    def has_permission(self, request, view):
        try:
            return (
                request.user
                and request.user.type == "ADMINISTRATOR"
            )
        except AttributeError as err:
            return False
