from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from nxtbn.cart.models import Cart, CartItem
from nxtbn.cart.api.storefront.serializers import CartAddUpdateSerializer, CartSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny

from nxtbn.cart.utils import get_or_create_cart, save_guest_cart
from nxtbn.core.utils import apply_exchange_rate, build_currency_amount, get_in_user_currency
from nxtbn.product.models import ProductVariant
from nxtbn.core.currency.backend import currency_Backend


class CartView(generics.GenericAPIView):
    """
    GET: Retrieve the current cart.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        cart, is_guest = get_or_create_cart(request)
        exchange_rate = currency_Backend().get_exchange_rate(self.request.currency)

        items = []
        total = 0

        if is_guest:
            # Handle guest cart stored in session
            for product_variant_id, item in cart.items():
                try:
                    product_variant = ProductVariant.objects.get(id=product_variant_id)
                    subtotal = product_variant.price * item['quantity']
                    total += subtotal
                    items.append({
                        'product_variant': {
                            'id': product_variant.id,
                            'alias': product_variant.alias,
                            'thumbnail': product_variant.variant_thumbnail(request),
                            'name': product_variant.get_descriptive_name(),
                            'price': apply_exchange_rate(product_variant.price, exchange_rate, self.request.currency, 'en_US'),
                            'stock': product_variant.stock,
                            'is_guest': is_guest
                        },
                        'quantity': item['quantity'],
                        'subtotal': apply_exchange_rate(subtotal, exchange_rate, self.request.currency, 'en_US'),
                    })
                except ProductVariant.DoesNotExist:
                    continue  # Optionally, handle missing product variants
        else:
            # Handle authenticated user's cart
            cart_items = cart.items.all()  # Assuming this is a reverse relation in Cart model
            for cart_item in cart_items:
                product_variant = cart_item.variant
                subtotal = product_variant.price * cart_item.quantity
                total += subtotal
                items.append({
                    'product_variant': {
                        'id': product_variant.id,
                        'alias': product_variant.alias,
                        'thumbnail': product_variant.variant_thumbnail(request),
                        'name': product_variant.get_descriptive_name(),
                        'price': apply_exchange_rate(product_variant.price, exchange_rate, self.request.currency, 'en_US'),
                        'stock': product_variant.stock,
                        'is_guest': is_guest
                    },
                    'quantity': cart_item.quantity,
                    'subtotal': apply_exchange_rate(subtotal, exchange_rate, self.request.currency, 'en_US'),
                })

        # Unified response for both guest and authenticated users
        unified_response = {
            'items': items,
            'total':  apply_exchange_rate(total, exchange_rate, self.request.currency, 'en_US'),
        }
        return Response(unified_response, status=status.HTTP_200_OK)



class AddToCartView(generics.CreateAPIView):
    """
    POST: Add an item to the cart.
    """
    permission_classes = [AllowAny]
    serializer_class = CartAddUpdateSerializer

    def post(self, request, *args, **kwargs):
        product_variant_id = request.data.get('product_variant_id')
        quantity = int(request.data.get('quantity', 1))

        product_variant = get_object_or_404(ProductVariant, id=product_variant_id)

        cart, is_guest = get_or_create_cart(request)

        if not is_guest:
            # Authenticated user
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
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Guest user
            cart = request.session.get('cart', {})
            if str(product_variant_id) in cart:
                cart[str(product_variant_id)]['quantity'] += quantity
            else:
                cart[str(product_variant_id)] = {
                    'quantity': quantity,
                    'price': str(product_variant.price)  # Ensure JSON serializable
                }
            save_guest_cart(request, cart)
            return Response({'message': 'Item added to cart successfully.'}, status=status.HTTP_200_OK)


class UpdateCartItemView(generics.UpdateAPIView):
    """
    PUT: Update the quantity of a cart item.
    """
    permission_classes = [AllowAny]
    serializer_class = CartAddUpdateSerializer

    def put(self, request, *args, **kwargs):
        product_variant_id = request.data.get('product_variant_id')
        quantity = int(request.data.get('quantity', 1))

        if quantity < 1:
            return Response({'error': 'Quantity must be at least 1.'}, status=status.HTTP_400_BAD_REQUEST)

        product_variant = get_object_or_404(ProductVariant, id=product_variant_id)

        cart, is_guest = get_or_create_cart(request)

        if not is_guest:
            # Authenticated user
            try:
                cart_item = CartItem.objects.get(cart=cart, variant=product_variant)
                cart_item.quantity = quantity
                cart_item.save()
                message = {'message': 'Cart item updated successfully.'}
                return Response(message, status=status.HTTP_200_OK)
            except CartItem.DoesNotExist:
                return Response({'error': 'Item not found in cart.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Guest user
            cart = request.session.get('cart', {})
            if str(product_variant_id) in cart:
                cart[str(product_variant_id)]['quantity'] = quantity
                save_guest_cart(request, cart)
                return Response({'message': 'Cart item updated successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Item not found in cart.'}, status=status.HTTP_404_NOT_FOUND)


class RemoveFromCartView(generics.DestroyAPIView):
    """
    DELETE: Remove an item from the cart.
    """
    permission_classes = [AllowAny]

    def delete(self, request, *args, **kwargs):
        product_variant_id = kwargs.get('product_variant_id')
        product_variant = get_object_or_404(ProductVariant, id=product_variant_id)

        cart, is_guest = get_or_create_cart(request)

        if not is_guest:
            # Authenticated user
            try:
                cart_item = CartItem.objects.get(cart=cart, variant=product_variant)
                cart_item.delete()
                serializer = CartSerializer(cart)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except CartItem.DoesNotExist:
                return Response({'error': 'Item not found in cart.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Guest user
            cart = request.session.get('cart', {})
            if str(product_variant_id) in cart:
                del cart[str(product_variant_id)]
                save_guest_cart(request, cart)
                return Response({'message': 'Item removed from cart successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Item not found in cart.'}, status=status.HTTP_404_NOT_FOUND)
