import graphene
from graphene_django import DjangoObjectType
from nxtbn.order.models import Address, Order

class AddressGraphType(DjangoObjectType):
    db_id = graphene.Int(source='id')
    class Meta:
        model = Address
        fields = (
            'id',
            'first_name',
            'last_name',
            'street_address',
            'city',
            'postal_code',
            'country',
            'phone_number',
            'email',
            'address_type',
        )


class OrderType(DjangoObjectType):
    db_id = graphene.Int(source='id')
    class Meta:
        model = Order
        fields = (
            'id',
            'order_number',
            'status',
            'shipping_address',
            'billing_address',
            'created_at',
            'last_modified',
            'total_price',
            'total_price_without_tax',
            'total_shipping_cost',
            'total_discounted_amount',
            'total_tax',
            'customer_currency',
            'currency_conversion_rate',
            'authorize_status',
            'charge_status',
            'promo_code',
            'gift_card',
            'payment_term',
            'due_date',
            'preferred_payment_method',
            'reservation_status',
            'note',
            'comment',
        )