from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.db import transaction


from nxtbn.discount.api.dashboard.serializers import PromoCodeBasicSerializer
from nxtbn.order import AddressType, OrderChargeStatus, OrderStatus
from nxtbn.order.api.storefront.serializers import AddressSerializer
from nxtbn.order.models import Address, Order, OrderLineItem
from nxtbn.payment.api.dashboard.serializers import BasicPaymentSerializer
from nxtbn.payment.models import Payment
from nxtbn.product.api.dashboard.serializers import ProductVariantSerializer
from nxtbn.product.models import ProductVariant
from nxtbn.users.api.dashboard.serializers import UserSerializer
from nxtbn.users.models import User

class LineVariantSerializer(serializers.ModelSerializer):
    variant_thumbnail = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    class Meta:
        model = ProductVariant
        fields = ['alias', 'name', 'sku', "variant_thumbnail", "price",]

    def get_variant_thumbnail(self, obj):
        return obj.variant_thumbnail(self.context.get('request'))
    
    def get_price(self, obj):
        return obj.humanize_total_price()

class OrderLineItemSerializer(serializers.ModelSerializer):
    variant = LineVariantSerializer()
    total_price = serializers.SerializerMethodField()
    price_per_unit = serializers.SerializerMethodField()
    class Meta:
        model = OrderLineItem
        fields = ('id', 'quantity', 'price_per_unit', 'total_price', "variant",)

    def get_total_price(self, obj):
        return obj.humanize_total_price()
    
    def get_price_per_unit(self, obj):
        return obj.humanize_price_per_unit()


class OrderSerializer(serializers.ModelSerializer):
    line_items = OrderLineItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()
    supplier = serializers.StringRelatedField(allow_null=True)
    shipping_address = serializers.StringRelatedField(allow_null=True)
    billing_address = serializers.StringRelatedField(allow_null=True)
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
            'note',
            'comment',
        )

class OrderListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    payment_method = serializers.CharField(source='get_payment_method')
    humanize_total_price = serializers.CharField()

    class Meta:
        model = Order
        fields = '__all__'




class OrderLineItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLineItem
        fields = ['variant', 'quantity', 'price_per_unit', 'currency', 'total_price_in_customer_currency']






class AddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street_address', 'city', 'state', 'postal_code', 'country', 'phone_number', 'first_name', 'last_name']

class CustomerCreateSerializer(serializers.ModelSerializer):
    address = AddressCreateSerializer(write_only=True)

    class Meta:
        model = User
        fields = ['id','full_name', 'first_name', 'last_name', 'phone_number', 'email', 'address']
        read_only_fields = ['id', 'full_name',]

    @transaction.atomic
    def create(self, validated_data):
        address_data = validated_data.pop('address')
        email = validated_data.get('email')
        username = email.split('@')[0]
        if User.objects.filter(username=username).exists():
            username = f"{username}_{User.objects.count()}"
        
        validated_data['username'] = username
        
        user = User.objects.create(**validated_data)
        Address.objects.create(
            user=user, 
            address_type=AddressType.DSA_DBA,
            **address_data
        )
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A customer with this email already exists.")
        return value
    


class OrderDetailsSerializer(serializers.ModelSerializer):
    line_items = OrderLineItemSerializer(many=True, read_only=True)
    shipping_address = AddressSerializer()
    billing_address =  AddressSerializer()
    total_price = serializers.SerializerMethodField()
    total_price_without_symbol = serializers.SerializerMethodField()
    total_shipping_cost = serializers.SerializerMethodField()
    total_discounted_amount = serializers.SerializerMethodField()
    total_tax = serializers.SerializerMethodField()
    due = serializers.SerializerMethodField()
    overcharged_amount = serializers.CharField(source='get_overcharged_amount')
    total_price_in_customer_currency = serializers.SerializerMethodField()
    user = UserSerializer()
    payment_method = serializers.CharField(source='get_payment_method')
    promo_code = PromoCodeBasicSerializer()
    payments = BasicPaymentSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'alias',
            'user',
            'supplier',
            'total_price',
            'total_price_without_symbol',
            'total_shipping_cost',
            'total_discounted_amount',
            'total_tax',
            'due',
            'overcharged_amount',
            'customer_currency',
            'total_price_in_customer_currency',
            'status',
            'authorize_status',
            'charge_status',
            'payment_method',
            'created_at',
            'shipping_address',
            'billing_address',
            'line_items',
            'promo_code',
            'gift_card',
            'due_date',
            'payment_term',
            'payments',
            'preferred_payment_method',
            'is_overdue',
        )

    def get_total_price(self, obj):
        return obj.humanize_total_price()
    
    def get_total_price_without_symbol(self, obj):
        return obj.humanize_total_price(locale='')
    
    def get_total_shipping_cost(self, obj):
        return obj.humanize_total_shipping_cost()
    
    def get_total_discounted_amount(self, obj):
        return obj.humanize_total_discounted_amount()
    
    def get_total_tax(self, obj):
        return obj.humanize_total_tax()

    def get_total_price_in_customer_currency(self, obj):
        return obj.total_price_in_customer_currency
    
    def get_due(self, obj):
        return obj.get_due()
    

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=OrderStatus.choices)

    class Meta:
        model = Order
        fields = ['status']

    def validate(self, attrs):
        order = self.instance

        current_status = order.status
        new_status = attrs.get('status')

        if new_status == OrderStatus.CANCELLED:
            if current_status == OrderStatus.CANCELLED:
                raise serializers.ValidationError(_("Order is already cancelled."))
            elif current_status not in [OrderStatus.PENDING, OrderStatus.APPROVED]:
                raise serializers.ValidationError(_(f"{current_status.value} orders cannot be cancelled."))
        
        if new_status == OrderStatus.PROCESSING:
            if current_status != OrderStatus.APPROVED:
                raise serializers.ValidationError(_("Only pending orders can be started to processing."))
            
        if new_status == OrderStatus.SHIPPED:
            if current_status == OrderStatus.CANCELLED:
                raise serializers.ValidationError(_("Cancelled orders cannot be shipped."))
            if current_status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
                raise serializers.ValidationError(_("Order is already shipped or delivered."))
            if current_status == OrderStatus.RETURNED:
                raise serializers.ValidationError(_("Returned orders cannot be re-shipped."))
            
        if new_status == OrderStatus.DELIVERED:
            if current_status == OrderStatus.CANCELLED:
                raise serializers.ValidationError(_("Cancelled orders cannot be delivered."))
            if current_status in [OrderStatus.DELIVERED]:
                raise serializers.ValidationError(_("Order is already delivered."))
            if current_status != OrderStatus.SHIPPED:
                raise serializers.ValidationError(_("Order must be shipped before mark it as delivered."))
        
        return attrs
    

class OrderPaymentMethodSerializer(serializers.ModelSerializer):
        preferred_payment_method = serializers.CharField()

        class Meta:
            model = Order
            fields = ['preferred_payment_method']

        def validate(self, attrs):
            order = self.instance
            if order.charge_status != OrderChargeStatus.DUE:
                raise serializers.ValidationError(_("Cannot change payment method for orders with charged funds."))
              
            return attrs