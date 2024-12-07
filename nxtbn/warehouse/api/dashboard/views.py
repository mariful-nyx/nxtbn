from rest_framework import viewsets
from rest_framework import generics
from nxtbn.warehouse.models import Warehouse, Stock, StockMovement
from nxtbn.warehouse.api.dashboard.serializers import WarehouseSerializer, StockSerializer, StockMovementSerializer, StockDetailViewSerializer, StockMovementDetailSerializer
from nxtbn.core.paginator import NxtbnPagination


from rest_framework import filters as drf_filters
import django_filters
from django_filters import rest_framework as filters



class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class StockFilter(filters.FilterSet):
    warehouse = filters.CharFilter(field_name='warehouse__name', lookup_expr='iexact')
    created_at = filters.DateTimeFromToRangeFilter(field_name='created_at')

    class Meta:
        model = Stock
        fields = [
            'warehouse',
            'created_at'
        ]
  
class StockFilterMixin:
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter
    ] 
    search_fields = [
        'warehouse__name',
        'product_variant__name'
    ]
    ordering_fields = [
        'created_at',
    ]
    filterset_class = StockFilter


class StockViewSet(StockFilterMixin, viewsets.ModelViewSet):
    queryset = Stock.objects.select_related('warehouse', 'product_variant').all()
    pagination_class = NxtbnPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StockDetailViewSerializer
        return StockSerializer





class StockMovementFilter(filters.FilterSet):
    from_warehouse = filters.CharFilter(field_name='from_warehouse__name', lookup_expr='iexact')
    to_warehouse = filters.CharFilter(field_name='to_warehouse__name', lookup_expr='iexact')
    movement_type = filters.CharFilter(field_name='movement_type', lookup_expr='iexact')
    created_at = filters.DateTimeFromToRangeFilter(field_name='created_at')

    class Meta:
        model = StockMovement
        fields = [
            'from_warehouse',
            'to_warehouse',
            'movement_type',
            'created_at'
        ]
  
class StockMovementFilterMixin:
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter
    ] 
    search_fields = [
        'from_warehouse__name',
        'to_warehouse__name',
        'movement_type',
        'product_variant__name'
    ]
    ordering_fields = [
        'created_at',
    ]
    filterset_class = StockMovementFilter


class StockMovementViewSet(StockMovementFilterMixin, viewsets.ModelViewSet):
    queryset = StockMovement.objects.select_related(
        'product_variant', 'from_warehouse', 'to_warehouse'
    ).all()
    pagination_class = NxtbnPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StockMovementDetailSerializer
        return StockMovementSerializer
