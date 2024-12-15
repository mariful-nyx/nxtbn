from django.urls import path
from nxtbn.purchase.api.dashboard import views

urlpatterns = [
    path('purchase-orders/', views.PurchaseOrderList.as_view(), name='purchase-order-list')
]


