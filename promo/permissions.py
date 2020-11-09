from rest_framework.permissions import BasePermission
from .models import Promo


class IsAdministration(BasePermission):
    def has_permission(self, request, view):
        try:
            return (request.user and request.user.type == "ADMINISTRATOR")
        except AttributeError as err:
            return False


class IsNormalUser(BasePermission):
    def has_permission(self, request, view):
        try:
            return (request.user and request.user.type == "NORMAL")
        except AttributeError as err:
            return False


class PromoRelatedToLoggedUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        promo = Promo.objects.get(pk=view.kwargs['pk'])
        return (user.pk == promo.user.pk)
