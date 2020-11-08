# from django.shortcuts import render
from rest_framework import viewsets, mixins
from promo.models import Promo
from promo.permissions import IsAdministration
from promo.serializers import PromoSerializer


class PromoViewSet(viewsets.ModelViewSet):
    model = Promo
    serializer_class = PromoSerializer
    queryset = Promo.objects.all()
    permission_classes = [
        IsAdministration,
    ]

