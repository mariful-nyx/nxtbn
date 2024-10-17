from django.urls import path
from nxtbn.checkout.api.storefront import views as checkout_view

urlpatterns = [
    path('checkout/', checkout_view.CheckoutView.as_view(), name='checkout'),
    path('clear-cart/', checkout_view.ClearCart.as_view(), name='clear-cart')
]
