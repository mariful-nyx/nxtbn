from rest_framework.routers import DefaultRouter
from django.urls import path
from nxtbn.warehouse.api.dashboard import views as warehouse_views

router = DefaultRouter()
router.register(r'warehouses', warehouse_views.WarehouseViewSet)
router.register(r'stocks', warehouse_views.StockViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('warehouse-wise-variant-stock/<int:variant_id>/', warehouse_views.WarehouseStockByVariantAPIView.as_view(), name='warehouse-wise-variant-stock'),
    path('upate-stock-warehosue-wise/<int:variant_id>/', warehouse_views.UpdateStockWarehouseWise.as_view(), name='update-stock-wirehouse-wise-variant-stock'),
    path('stock-reservation-list/', warehouse_views.StockReservationListAPIView.as_view(), name='update-stock-warehouse-wise-variant-stock'),
]
