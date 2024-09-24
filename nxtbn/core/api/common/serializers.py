from rest_framework import serializers

class VariantQuantitySerializer(serializers.Serializer):
    alias = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)

class PriceAndNameSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.CharField()

class OrderEstimateSerializer(serializers.Serializer):
    fixed_shipping_amount = PriceAndNameSerializer(required=False)
    variants = serializers.ListSerializer(child=VariantQuantitySerializer())
