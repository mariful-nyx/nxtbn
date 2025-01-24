

import graphene

from nxtbn.cart.models import Cart
from nxtbn.cart.storefront_types import CartItemType, CartType


class AdminCartQuery(graphene.ObjectType):
    all_carts = graphene.List(CartType)
    
    cart_by_user = graphene.Field(CartType, user_id=graphene.ID(required=True))
    
    items_in_cart = graphene.List(CartItemType, cart_id=graphene.ID(required=True))

    def resolve_all_carts(self, info, **kwargs):
        return Cart.objects.all()

    def resolve_cart_by_user(self, info, user_id):
        try:
            return Cart.objects.get(user_id=user_id)
        except Cart.DoesNotExist:
            return None

    def resolve_items_in_cart(self, info, cart_id):
        try:
            cart = Cart.objects.get(id=cart_id)
            return cart.items.all()
        except Cart.DoesNotExist:
            return None
