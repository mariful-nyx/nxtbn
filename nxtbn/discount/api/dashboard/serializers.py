from rest_framework import serializers
from nxtbn.discount.models import PromoCode


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = '__all__'