# from django.shortcuts import render
from rest_framework import viewsets, generics
from promo.models import Promo
from promo.permissions import IsAdministration, IsNormalUser
from promo.serializers import PromoSerializer


class PromoViewSet(viewsets.ModelViewSet):
    model = Promo
    serializer_class = PromoSerializer
    queryset = Promo.objects.all()
    permission_classes = [
        IsAdministration,
    ]


class PromoMeListView(generics.ListAPIView):
    model = Promo
    serializer_class = PromoSerializer
    permission_classes = [
        IsNormalUser,
    ]

    def get_queryset(self):
        return Promo.objects.filter(user=self.request.user.pk)
