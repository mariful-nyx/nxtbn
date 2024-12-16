from rest_framework import viewsets
from rest_framework import generics, status
from nxtbn.product.models import ProductVariant
from nxtbn.warehouse.models import Warehouse, Stock
from nxtbn.warehouse.api.dashboard.serializers import WarehouseSerializer, StockSerializer, StockDetailViewSerializer
from nxtbn.core.paginator import NxtbnPagination


from rest_framework import filters as drf_filters
from rest_framework.views import APIView
import django_filters
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django.db.models.functions import Coalesce
from django.db.models import F



class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

    def get_queryset(self):
        no_pagination = self.request.query_params.get('no_pagination', None)
        if no_pagination == 'true':
            self.pagination_class = None

        return super().get_queryset()


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




class WarehouseStockByVariantAPIView(APIView):
    def get(self, request, variant_id):
        try:
            # Fetch the product variant
            product_variant = ProductVariant.objects.get(id=variant_id)
        except ProductVariant.DoesNotExist:
            return Response({"error": "Variant not found."}, status=status.HTTP_404_NOT_FOUND)

        # Annotate warehouses with stock data for the given variant
        warehouses = Warehouse.objects.annotate(
            total_quantity=Coalesce(
                Stock.objects.filter(warehouse=F('id'), product_variant=product_variant)
                .values('quantity')[:1], 0
            ),
            reserved_quantity=Coalesce(
                Stock.objects.filter(warehouse=F('id'), product_variant=product_variant)
                .values('reserved')[:1], 0
            )
        )

        # Prepare the response data
        data = []
        for warehouse in warehouses:
            # Calculate available quantity
            available_quantity = warehouse.total_quantity - warehouse.reserved_quantity
            data.append({
                "warehouse_name": warehouse.name,
                "total_quantity": warehouse.total_quantity,
                "reserved_quantity": warehouse.reserved_quantity,
                "available_quantity": available_quantity
            })

        return Response(data)