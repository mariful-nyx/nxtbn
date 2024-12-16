from django.urls import path
from rest_framework.routers import DefaultRouter
from nxtbn.purchase.api.dashboard import views

router = DefaultRouter()

router.register(r'purchase-orders', views.PurchaseOrderViewSet)

urlpatterns = router.urls




