from rest_framework.routers import DefaultRouter
from nxtbn.warehouse.api.dashboard.views import WarehouseViewSet, StockViewSet


router = DefaultRouter()
router.register(r'warehouses', WarehouseViewSet)
router.register(r'stocks', StockViewSet)

urlpatterns = router.urls