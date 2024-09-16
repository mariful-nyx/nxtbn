from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.db import transaction


from nxtbn.order import OrderStatus
from nxtbn.order.models import Order, OrderLineItem
from nxtbn.payment.models import Payment
from nxtbn.product.api.dashboard.serializers import ProductVariantSerializer


class OrderLineItemSerializer(serializers.ModelSerializer):
    variant = ProductVariantSerializer(read_only=True)
    class Meta:
        model = OrderLineItem
        fields = ('id', 'variant', 'quantity', 'price_per_unit', 'total_price',)


class OrderSerializer(serializers.ModelSerializer):
    line_items = OrderLineItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()
    supplier = serializers.StringRelatedField(allow_null=True)
    shipping_address = serializers.StringRelatedField(allow_null=True)
    billing_address = serializers.StringRelatedField(allow_null=True)
    promo_code = serializers.StringRelatedField(allow_null=True)
    gift_card = serializers.StringRelatedField(allow_null=True)
    payment_method = serializers.CharField(source='get_payment_method')

    class Meta:
        model = Order
        fields = (
            'id',
            'alias',
            'user',
            'supplier',
            'payment_method',
            'shipping_address',
            'billing_address',
            'total_price',
            'status',
            'authorize_status',
            'charge_status',
            'promo_code',
            'gift_card',
            'line_items',
        )

class OrderListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    payment_method = serializers.CharField(source='get_payment_method')

    class Meta:
        model = Order
        fields = '__all__'




class OrderLineItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLineItem
        fields = ['variant', 'quantity', 'price_per_unit', 'currency', 'total_price_in_customer_currency']

class OrderCreateSerializer(serializers.ModelSerializer):
    line_items = OrderLineItemCreateSerializer(many=True)  # To handle multiple line items
    
    class Meta:
        model = Order
        fields = [
            'user',
            'supplier',
            'shipping_address',
            'billing_address', 
            'total_price_in_customer_currency',
            'status',
            'authorize_status', 
            'charge_status',
            'promo_code',
            'gift_card',
            'is_due',
            'line_items'
        ]

    def create(self, validated_data):
        line_items_data = validated_data.pop('line_items')
        order = Order.objects.create(
            **validated_data,
        )
        
        # Create line items for the order
        for line_item_data in line_items_data:
            OrderLineItem.objects.create(order=order, **line_item_data)
        
        return order
