from rest_framework import serializers

from nxtbn.discount.models import PromoCode
from nxtbn.product.models import Product
from nxtbn.users import UserRole

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
    state = serializers.CharField(required=False)
    street_address = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)

class OrderEstimateSerializer(serializers.Serializer):
    shipping_address = ShippingAddressSerializer(required=False)
    billing_address = ShippingAddressSerializer(required=False)
    shipping_address_id = serializers.IntegerField(required=False)
    billing_address_id = serializers.IntegerField(required=False)

    shipping_method_id = serializers.IntegerField(required=False)
    custom_shipping_amount = PriceAndNameSerializer(required=False)

    custom_discount_amount = PriceAndNameSerializer(required=False)
    promocode = serializers.CharField(required=False)
    variants = serializers.ListSerializer(child=VariantQuantitySerializer(), required=True)
    customer_id = serializers.IntegerField(required=False) # if order is created by admin
    note = serializers.CharField(required=False)

    def validate_variants(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("You must add one or more products to your cart.")
        return value
    
    def validate_custom_discount_amount(self, value):
        if value and not value.get('price'):
            raise serializers.ValidationError("Discount amount is required.")
        
        if self.context['request'].user.role == UserRole.CUSTOMER:
            raise serializers.ValidationError("You are not authorized to apply discount. Only staff can apply discount.")
        return value
        