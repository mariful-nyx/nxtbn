from rest_framework import serializers

from nxtbn.discount.models import PromoCode

class VariantQuantitySerializer(serializers.Serializer):
    alias = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)

class PriceAndNameSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.CharField()

class ShippingAddressSerializer(serializers.Serializer):
    city = serializers.CharField(required=False)
    postal_code = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    region = serializers.CharField(required=False)

class OrderEstimateSerializer(serializers.Serializer):
    shipping_address = ShippingAddressSerializer(required=False)
    shipping_method_id = serializers.IntegerField(required=False)
    custom_shipping_amount = PriceAndNameSerializer(required=False)

    custom_discount_amount = PriceAndNameSerializer(required=False)
    promocode = serializers.CharField(required=False)
    variants = serializers.ListSerializer(child=VariantQuantitySerializer(), required=True)

    def validate_promocode(self, value):
        if value:
            try:
                promocode = PromoCode.objects.get(code=value.upper(), active=True)
                if not promocode.is_valid():
                    raise serializers.ValidationError("Invalid or expired promo code.")
                return promocode
            except PromoCode.DoesNotExist:
                raise serializers.ValidationError("Promo code does not exist.")
        return None