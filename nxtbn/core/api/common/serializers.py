from rest_framework import serializers

class VariantQuantitySerializer(serializers.Serializer):
    alias = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)

class OrderEstimateSerializer(serializers.Serializer):
    variants = serializers.ListSerializer(child=VariantQuantitySerializer())
