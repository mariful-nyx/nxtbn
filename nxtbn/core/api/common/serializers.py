from rest_framework import serializers

class VariantQuantitySerializer(serializers.Serializer):
    alias = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)

class PriceAndNameSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.CharField()

class ShippingAddressSerializer(serializers.Serializer):
    country = serializers.CharField()
    city = serializers.CharField()


class OrderEstimateSerializer(serializers.Serializer):
    """
    Serializer for estimating order shipping costs and details.

    This serializer handles the following business rules:

    - Only one of 'shipping_address', 'customer_id', or 'fixed_shipping_amount' can be present in the payload.
    - If 'shipping_address' is provided, it will be used for calculating shipping costs.
    - If both 'shipping_address' and 'customer_id' are absent, the 'fixed_shipping_amount' will be used if provided.
    - If two or all three fields are provided, a validation error will be raised.

    Fields:
    - shipping_address: Optional. The shipping address for the order.
    - customer_id: Optional. The ID of the customer, used to retrieve their shipping address.
    - fixed_shipping_amount: Optional. A fixed shipping rate that may be used if applicable.
    - variants: A list of variants and their quantities included in the order.
    """

    shipping_address = ShippingAddressSerializer(required=False)
    customer_id = serializers.CharField(required=False)
    fixed_shipping_amount = PriceAndNameSerializer(required=False)
    variants = serializers.ListSerializer(child=VariantQuantitySerializer(), required=True)

    def validate(self, attrs):
        shipping_address = attrs.get('shipping_address')
        customer_id = attrs.get('customer_id')
        fixed_shipping_amount = attrs.get('fixed_shipping_amount')

        # Count how many of the fields are present
        fields_present = sum([bool(shipping_address), bool(customer_id), bool(fixed_shipping_amount)])

        if fields_present > 1:
            raise serializers.ValidationError("Only one of 'shipping_address', 'customer_id', or 'fixed_shipping_amount' can be provided.")

        return attrs