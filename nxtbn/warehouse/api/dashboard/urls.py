from rest_framework.routers import DefaultRouter
from django.urls import path
from nxtbn.warehouse.api.dashboard.views import WarehouseViewSet, StockViewSet, WarehouseStockByVariantAPIView, UpdateStockWarehouseWise

router = DefaultRouter()
router.register(r'warehouses', WarehouseViewSet)
router.register(r'stocks', StockViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('warehouse-wise-variant-stock/<int:variant_id>/', WarehouseStockByVariantAPIView.as_view(), name='warehouse-wise-variant-stock'),
    path('upate-stock-warehosue-wise/<int:variant_id>/', UpdateStockWarehouseWise.as_view(), name='update-stock-wirehouse-wise-variant-stock'),
]
