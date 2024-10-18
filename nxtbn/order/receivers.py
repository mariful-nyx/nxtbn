from django.dispatch import receiver
from nxtbn.core.signal_initiators import order_created

@receiver(order_created)
def rectify_cart_on_order_create(sender, order, request, **kwargs):
    """
    Remove item that is in the order from the cart, unordered items will remain.
    """
    print('Order created signal received=======================================================.')
   
