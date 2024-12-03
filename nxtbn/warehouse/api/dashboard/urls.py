from rest_framework.routers import DefaultRouter
from nxtbn.warehouse.api.dashboard.views import WarehouseViewSet, StockViewSet, StockMovementViewSet

router = DefaultRouter()
router.register(r'warehouses', WarehouseViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'stock-movements', StockMovementViewSet)

urlpatterns = router.urls
