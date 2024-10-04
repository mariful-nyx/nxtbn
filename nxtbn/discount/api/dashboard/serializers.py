from rest_framework import serializers
from nxtbn.discount.models import PromoCode


class PromoCodeSerializer(serializers.ModelSerializer):
    total_redemptions = serializers.IntegerField(read_only=True, source='get_total_redemptions')
    total_applicable_products = serializers.IntegerField(read_only=True, source='get_total_applicable_products')
    total_specific_customers = serializers.IntegerField(read_only=True, source='get_total_specific_customers')
    class Meta:
        model = PromoCode
        exclude = ('applicable_products', 'specific_customers',)