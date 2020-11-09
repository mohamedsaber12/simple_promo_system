# from django.shortcuts import render
from rest_framework import viewsets, generics
from promo.models import Promo, PromoUse
from promo.permissions import IsAdministration, IsNormalUser, PromoRelatedToLoggedUser
from promo.serializers import PromoSerializer, PromoPointsSerializer, PromoPointsUseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


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


class PromoPointsDetailView(generics.RetrieveUpdateAPIView):
    model = Promo
    serializer_class = PromoPointsSerializer
    permission_classes = [IsNormalUser, PromoRelatedToLoggedUser]
    queryset = Promo.objects.all()


class PromoPointsUse(APIView):
    permission_classes = [IsNormalUser, PromoRelatedToLoggedUser]

    def post(self, request, pk):
        serializer = PromoPointsUseSerializer(data=request.data,
                                              context={"pk": pk})
        serializer.is_valid(raise_exception=True)

        promo = get_object_or_404(Promo, pk=pk)
        PromoUse.objects.create(
            promo=promo,
            number_of_points=serializer.validated_data.get("points_to_use"))
        promo.refresh_from_db()
        return Response({
            "message": "success",
            "remaining_points": promo.remaining_points
        })
