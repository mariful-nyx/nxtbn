import graphene
from graphql import GraphQLError
from graphene_django.types import DjangoObjectType
from nxtbn.product.models import ProductVariant
from nxtbn.cart.models import Cart, CartItem 
from nxtbn.core.currency.backend import currency_Backend
from nxtbn.graph_api.types import CartType, ProductVariantType 
from nxtbn.cart.utils import get_or_create_cart, save_guest_cart  

class AddToCartMutation(graphene.Mutation):
    class Arguments:
        product_variant_id = graphene.ID(required=True)
        quantity = graphene.Int(required=False)

    success = graphene.Boolean()
    message = graphene.String()
    cart = graphene.Field(CartType)

    def mutate(self, info, product_variant_id, quantity=1):
        try:
            product_variant = ProductVariant.objects.get(id=product_variant_id)
        except ProductVariant.DoesNotExist:
            raise GraphQLError("Product variant not found")

        cart, is_guest = get_or_create_cart(info.context)

        if not is_guest:
            # Authenticated user - Add or update the cart item
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                variant=product_variant
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            else:
                cart_item.quantity = quantity
                cart_item.save()
            return AddToCartMutation(success=True, message="Item added to cart", cart=cart)

        else:
            # Guest user - Add item to session cart
            cart_data = info.context.session.get('cart', {})
            if str(product_variant_id) in cart_data:
                cart_data[str(product_variant_id)]['quantity'] += quantity
            else:
                cart_data[str(product_variant_id)] = {
                    'quantity': quantity,
                    'price': str(product_variant.price)  # Ensure JSON serializable
                }
            save_guest_cart(info.context, cart_data)
            return AddToCartMutation(success=True, message="Item added to cart", cart=None)




class CartMutation(graphene.ObjectType):
    add_to_cart = AddToCartMutation.Field()

