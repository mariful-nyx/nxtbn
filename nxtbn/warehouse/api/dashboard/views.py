from rest_framework import viewsets
from nxtbn.warehouse.models import Warehouse, Stock, StockMovement
from nxtbn.warehouse.api.dashboard.serializers import WarehouseSerializer, StockSerializer, StockMovementSerializer

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.select_related('warehouse', 'product_variant').all()
    serializer_class = StockSerializer

class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.select_related(
        'product_variant', 'from_warehouse', 'to_warehouse'
    ).all()
    serializer_class = StockMovementSerializer
