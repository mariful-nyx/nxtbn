from rest_framework import serializers

from nxtbn.discount.models import PromoCode
from nxtbn.product.models import Product

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
    customer_id = serializers.IntegerField(required=False)

    def validate_variants(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("You must add one or more products to your cart.")
        return value