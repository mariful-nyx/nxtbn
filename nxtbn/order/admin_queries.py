import graphene
from graphene_django.filter import DjangoFilterConnectionField

from nxtbn.core.admin_permissions import check_user_permissions
from nxtbn.order.admin_types import OrderType
from nxtbn.order.models import Address, Order
from nxtbn.users import UserRole


class AdminOrderQuery(graphene.ObjectType):
    orders = DjangoFilterConnectionField(OrderType)
    order = graphene.Field(OrderType, id=graphene.Int(required=True))

    # all_addresses = graphene.List(AddressGraphType)
    # address = graphene.Field(AddressGraphType, id=graphene.Int(required=True))

    def resolve_orders(self, info, **kwargs):
        check_user_permissions(info, any_staff=True)
        return Order.objects.all()
    
    def resolve_order(self, info, id):
        check_user_permissions(info, any_staff=True)
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            raise Exception("Order not found")
        
        return order

    def resolve_addresses(self, info):
        check_user_permissions(info, any_staff=True)
        return Address.objects.all()

    def resolve_address(self, info, id):
        check_user_permissions(info, any_staff=True)
        try:
            address = Address.objects.get(id=id)
        except Address.DoesNotExist:
            raise Exception("Address not found")
        
        return address
