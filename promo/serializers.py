from rest_framework import serializers
from promo.models import Promo
from django.shortcuts import get_object_or_404


class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = (
            "id",
            "user",
            "promo_type",
            "promo_code",
            "creation_time",
            "start_date",
            "end_date",
            "promo_amount",
            "is_active",
        )


class PromoPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = (
            "id",
            "promo_code",
            "creation_time",
            "start_date",
            "end_date",
            "promo_amount",
            "total_used_points",
            "remaining_points",
        )


class PromoPointsUseSerializer(serializers.Serializer):
    points_to_use = serializers.IntegerField(required=True, min_value=0)

    def validate(self, data):
        points_to_use = data.get("points_to_use")
        pk = self.context.get("pk")
        promo = get_object_or_404(Promo, pk=pk)
        if points_to_use > promo.remaining_points:
            raise serializers.ValidationError({
                "points_to_use":
                f"remaining points is less than {points_to_use} it's {promo.remaining_points}"
            })

        return data