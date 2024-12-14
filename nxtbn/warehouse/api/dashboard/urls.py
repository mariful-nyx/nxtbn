from rest_framework.routers import DefaultRouter
from django.urls import path
from nxtbn.warehouse.api.dashboard.views import WarehouseViewSet, StockViewSet, WarehouseStockByVariantAPIView

router = DefaultRouter()
router.register(r'warehouses', WarehouseViewSet)
router.register(r'stocks', StockViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('warehouse-wise-variant-stock/<int:variant_id>/', WarehouseStockByVariantAPIView.as_view(), name='warehouse-wise-variant-stock'),
]
