
from nxtbn.product.models import ProductVariant
from nxtbn.cart.models import Cart, CartItem

from django.shortcuts import get_object_or_404

def get_or_create_cart(request):
    """
    Retrieves the cart for the authenticated user or creates a new guest cart.
    Returns a tuple: (cart_object, is_guest)
    """
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart, False
    else:
        # For guest users, retrieve the cart from the session
        cart = request.session.get('cart', {})
        return cart, True

def save_guest_cart(request, cart):
    """
    Saves the guest cart back to the session.
    """
    request.session['cart'] = cart
    request.session.modified = True

def merge_carts(request, user):
    """
    Merges the guest cart stored in the session with the authenticated user's cart.
    """
    session_cart = request.session.get('cart', {})
    if not session_cart:
        return

    cart, created = Cart.objects.get_or_create(user=user)

    for product_variant_id, item in session_cart.items():
        product_variant = get_object_or_404(ProductVariant, id=product_variant_id)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_variant=product_variant
        )
        if not created:
            cart_item.quantity += item.get('quantity', 1)
            cart_item.save()
        else:
            cart_item.quantity = item.get('quantity', 1)
            cart_item.save()

    # Clear the session cart after merging
    request.session['cart'] = {}
