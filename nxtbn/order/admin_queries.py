import graphene

from nxtbn.order.admin_types import OrderType
from nxtbn.order.storefront_types import AddressGraphType
from nxtbn.order.models import Address


class AdminOrderQuery(graphene.ObjectType):
    all_orders = graphene.List(OrderType)
    order = graphene.Field(OrderType, id=graphene.Int(required=True))

    all_addresses = graphene.List(AddressGraphType)
    address = graphene.Field(AddressGraphType, id=graphene.Int(required=True))

    def resolve_all_addresses(self, info):
        return Address.objects.all()

    def resolve_address(self, info, id):
        try:
            address = Address.objects.get(id=id)
        except Address.DoesNotExist:
            raise Exception("Address not found")
        
        return address
