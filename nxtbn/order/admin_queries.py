import graphene
from graphene_django.filter import DjangoFilterConnectionField

from nxtbn.core.admin_permissions import gql_store_admin_required
from nxtbn.order.admin_types import OrderType
from nxtbn.order.models import Address, Order
from nxtbn.users import UserRole


class AdminOrderQuery(graphene.ObjectType):
    orders = DjangoFilterConnectionField(OrderType)
    order = graphene.Field(OrderType, id=graphene.Int(required=True))

   

    @gql_store_admin_required
    def resolve_orders(self, info, **kwargs):
        return Order.objects.all()
    
    @gql_store_admin_required
    def resolve_order(self, info, id):
        try:
            order = Order.objects.get(id=id)
        except Order.DoesNotExist:
            raise Exception("Order not found")
        
        return order