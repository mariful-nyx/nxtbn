from django.urls import path
from nxtbn.order.api.storefront import views as order_views

urlpatterns = [
    path('orders/', order_views.OrderListView.as_view(), name='order-list'),
    path('eastimate/', order_views.OrderEastimateAPIView.as_view(), name='order-eastimate'),
    path('create/', order_views.OrderCreateAPIView.as_view(), name='order-create'),
]
