
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from nxtbn.cart.utils import merge_carts

@receiver(user_logged_in)
def handle_user_logged_in(sender, user, request, **kwargs):
    """
    Signal handler that merges the guest cart with the authenticated user's cart upon login.
    """
    merge_carts(request, user)
