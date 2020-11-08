from rest_framework import serializers
from promo.models import Promo


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
