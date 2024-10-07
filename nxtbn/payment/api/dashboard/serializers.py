from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.db import transaction

from nxtbn.core.utils import build_currency_subunit
from nxtbn.order import OrderAuthorizationStatus, OrderChargeStatus, OrderStatus
from nxtbn.order.models import Order
from nxtbn.payment.models import Payment

class RefundSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(write_only=True, max_digits=4, decimal_places=2)
    class Meta:
        model = Payment
        fields = ['amount']

    def update(self, instance, validated_data):
        amount = validated_data.get('amount', '') # if null, then full refund, if amount, partial refund
        instance.refund_payment(amount)
        return instance

class BasicPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'payment_amount', 'payment_status', 'gateway_name', 'created_at',]


class PaymentCreateSerializer(serializers.ModelSerializer):
    order = serializers.CharField(write_only=True)
    payment_amount = serializers.DecimalField(required=True, max_digits=10, decimal_places=3)
    force_it = serializers.BooleanField(write_only=True, default=False)

    class Meta:
        model = Payment
        fields = [
            'order',
            'payment_method',
            'transaction_id',
            'payment_amount',
            'paid_at',
            'force_it',
        ]
        read_only_fields = ['order', 'user']  # You might want to set some fields as read-only

    def validate_order(self, value):
        try:
            order = Order.objects.get(alias=value)  # Assuming order has an alias field
        except Order.DoesNotExist:
            raise serializers.ValidationError(f"Order with alias '{value}' does not exist.")
        return order

    def create(self, validated_data):
        forice_it = validated_data.pop('force_it', False)
        order = validated_data.get('order')

        order_total_subunit = order.total_price

        validated_data['user'] = order.user
        validated_data['currency'] = order.currency
        validated_data['payment_amount'] =  build_currency_subunit(validated_data['payment_amount'], order.currency)

    
        if validated_data['payment_amount'] < order_total_subunit:
            if not forice_it:
                raise serializers.ValidationError(_("Payment amount is less than the total order price."))
        
            order.charge_status = OrderChargeStatus.PARTIAL
            order.authorization_status = OrderAuthorizationStatus.PARTIAL

        if validated_data['payment_amount'] > order_total_subunit:
            if not forice_it:
                raise serializers.ValidationError(_("Payment amount exceeds the total order price."))
            order.charge_status = OrderChargeStatus.OVERCHARGED
        
        if validated_data['payment_amount'] == order_total_subunit:
            order.charge_status = OrderChargeStatus.FULL
            order.authorization_status = OrderAuthorizationStatus.FULL

        payment = Payment.objects.create(**validated_data)
        order.save()

        return payment