from django.urls import path
from nxtbn.core.api.common.views import OrderEstimateAPIView
from nxtbn.core.api.common import views as core_views

urlpatterns = [
    path('order/eastimate/', core_views.OrderEstimateAPIView.as_view(), name='order-estimate'),
]
