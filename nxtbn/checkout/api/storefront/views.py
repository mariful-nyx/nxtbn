from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions  import AllowAny
from rest_framework.exceptions import APIException

from nxtbn.order.models import Order
from nxtbn.order.api.dashboard.serializers import OrderSerializer
from nxtbn.order.proccesor.views import OrderProccessorAPIView
from nxtbn.cart.models import Cart, CartItem
from nxtbn.cart.api.storefront.serializers import CartSerializer, CartItemSerializer
from nxtbn.cart.utils import get_object_or_404, get_or_create_cart, save_guest_cart
from nxtbn.checkout.api.storefront.serializers import CheckoutSerializer
from django.contrib.auth import get_user_model

class CheckoutView(OrderProccessorAPIView):
    permission_classes = [AllowAny]
    create_order = True


class ClearCart(generics.DestroyAPIView):
    permission_classes = [AllowAny]

    def delete(self, request, *args, **kwargs):
        cart, is_guest = get_or_create_cart(request)

        if not is_guest:
            # Authenticated user
            try:
                cart_item = CartItem.objects.all()
                cart_item.delete()
                return Response(status=status.HTTP_200_OK)
            except CartItem.DoesNotExist:
                return Response({'error': 'Item not found in cart.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Guest user
            cart = request.session.get('cart', {})
            if cart:
                del cart
                save_guest_cart(request, {})
                return Response({'message': 'Item removed from cart successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Item not found in cart.'}, status=status.HTTP_404_NOT_FOUND)


        


