from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.db import transaction


from nxtbn.order import AddressType, OrderStatus
from nxtbn.order.models import Address, Order, OrderLineItem
from nxtbn.payment.models import Payment
from nxtbn.product.api.dashboard.serializers import ProductVariantSerializer
from nxtbn.users.api.dashboard.serializers import UserSerializer
from nxtbn.users.models import User


class OrderLineItemSerializer(serializers.ModelSerializer):
    # variant = ProductVariantSerializer(read_only=True)
    class Meta:
        model = OrderLineItem
        fields = ('id', 'quantity', 'price_per_unit', 'total_price',)


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
    shipping_address = serializers.StringRelatedField()
    billing_address = serializers.StringRelatedField()
    total_price = serializers.SerializerMethodField()
    total_price_in_customer_currency = serializers.SerializerMethodField()
    user = UserSerializer()

    class Meta:
        model = Order
        fields = (
            'id',
            'alias',
            'user',
            'supplier',
            'total_price',
            'customer_currency',
            'total_price_in_customer_currency',
            'status',
            'created_at',
            'shipping_address',
            'billing_address',
            'line_items',
            'promo_code',
            'gift_card',
            'due_date',
        )

    def get_total_price(self, obj):
        return obj.humanize_total_price()

    def get_total_price_in_customer_currency(self, obj):
        return obj.total_price_in_customer_currency 