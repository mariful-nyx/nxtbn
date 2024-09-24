from rest_framework import serializers

class VariantQuantitySerializer(serializers.Serializer):
    alias = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)

class PriceAndNameSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.CharField()


class OrderEstimateSerializer(serializers.Serializer):
    fixed_discount_amount = PriceAndNameSerializer(required=False)
    shipping_rate_id = serializers.IntegerField(required=False)
    fixed_shipping_amount = PriceAndNameSerializer(required=False)
    variants = serializers.ListSerializer(child=VariantQuantitySerializer(), required=True)