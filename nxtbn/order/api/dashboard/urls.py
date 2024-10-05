from django.urls import path

from nxtbn.order.api.dashboard import views as order_views


urlpatterns = [
    path('orders/', order_views.OrderListView.as_view(), name='order-list'),
    path('orders/create/', order_views.OrderCreateView.as_view(), name='order-create'),
    path('orders/eastimate/', order_views.OrderEastimateView.as_view(), name='order-eastimate'),
    path('create-customer/', order_views.CreateCustomAPIView.as_view(), name='create-customer'),
    path('orders/<uuid:alias>/', order_views.OrderDetailView.as_view(), name='order-detail'),
    path('stats/', order_views.BasicStatsView.as_view(), name='basic-stats'),
]
