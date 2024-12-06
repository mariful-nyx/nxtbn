from rest_framework import viewsets
from rest_framework import generics
from nxtbn.warehouse.models import Warehouse, Stock, StockMovement
from nxtbn.warehouse.api.dashboard.serializers import WarehouseSerializer, StockSerializer, StockMovementSerializer, StockDetailViewSerializer, StockMovementDetailSerializer
from nxtbn.core.paginator import NxtbnPagination


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.select_related('warehouse', 'product_variant').all()
    pagination_class = NxtbnPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StockDetailViewSerializer
        return StockSerializer


class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.select_related(
        'product_variant', 'from_warehouse', 'to_warehouse'
    ).all()
    pagination_class = NxtbnPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StockMovementDetailSerializer
        return StockMovementSerializer
