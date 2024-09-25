from rest_framework import serializers

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
    fixed_shipping_amount = PriceAndNameSerializer(required=False)
    fixed_discount_amount = PriceAndNameSerializer(required=False)
    variants = serializers.ListSerializer(child=VariantQuantitySerializer(), required=True)