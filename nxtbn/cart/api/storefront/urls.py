from django.urls import path

from nxtbn.cart.api.storefront import views as cart_views

urlpatterns = [
    path('carts/', cart_views.CartView.as_view(), name='cart-list'),
    path('carts/add/', cart_views.AddToCartView.as_view(), name='cart-add'),
    path('carts/remove/', cart_views.RemoveFromCartView.as_view(), name='cart-remove'),
    path('carts/update/', cart_views.UpdateCartItemView.as_view(), name='cart-update'),
]