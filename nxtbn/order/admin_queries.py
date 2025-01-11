import graphene
from graphene_django.filter import DjangoFilterConnectionField

from nxtbn.order.admin_types import OrderType
from nxtbn.order.storefront_types import AddressGraphType
from nxtbn.order.models import Address, Order


class AdminOrderQuery(graphene.ObjectType):
    all_orders = DjangoFilterConnectionField(OrderType)
    order = graphene.Field(OrderType, id=graphene.Int(required=True))

    all_addresses = graphene.List(AddressGraphType)
    address = graphene.Field(AddressGraphType, id=graphene.Int(required=True))

    def resolve_all_orders(self, info, **kwargs):
        return Order.objects.all()
    
    def resolve_order(self, info, id):
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            raise Exception("Order not found")
        
        return order

    def resolve_all_addresses(self, info):
        return Address.objects.all()

    def resolve_address(self, info, id):
        try:
            address = Address.objects.get(id=id)
        except Address.DoesNotExist:
            raise Exception("Address not found")
        
        return address
