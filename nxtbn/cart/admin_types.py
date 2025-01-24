import graphene
from graphene_django.types import DjangoObjectType
from nxtbn.cart.models import Cart, CartItem


class CartItemType(DjangoObjectType):
    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'variant', 'quantity', 'created_at', 'updated_at')


class CartType(DjangoObjectType):
    class Meta:
        model = Cart
        fields = ('id', 'user', 'items', 'created_at', 'updated_at')

    total_items = graphene.Int()

    def resolve_total_items(self, info):
        return sum(item.quantity for item in self.items.all())


