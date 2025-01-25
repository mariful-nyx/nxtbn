import graphene
from graphene import relay

from graphene_django.types import DjangoObjectType
from nxtbn.cart.models import Cart, CartItem
from nxtbn.users.admin_types import AdminUserType


class CartItemType(DjangoObjectType):
    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'variant', 'quantity', 'created_at', 'updated_at')


class CartType(DjangoObjectType):
    user = AdminUserType()
    total_items = graphene.Int()
    db_id = graphene.ID(source='id')
    class Meta:
        model = Cart
        fields = ('id', 'user', 'items', 'created_at', 'updated_at')
        interfaces = (relay.Node,)
        filter_fields = {
            'user__id': ['exact'],
            'created_at': ['exact', 'gte', 'lte'], 
            'updated_at': ['exact', 'gte', 'lte'],
        }

    def resolve_total_items(self, info):
        return sum(item.quantity for item in self.items.all())


