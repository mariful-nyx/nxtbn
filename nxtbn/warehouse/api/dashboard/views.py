
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import generics, status
from nxtbn.order.models import Order
from nxtbn.product.models import ProductVariant
from nxtbn.warehouse.models import StockReservation, StockTransfer, Warehouse, Stock
from nxtbn.warehouse.api.dashboard.serializers import StockReservationSerializer, StockTransferSerializer, StockUpdateSerializer, MergeStockReservationSerializer, WarehouseSerializer, StockSerializer, StockDetailViewSerializer
from nxtbn.core.paginator import NxtbnPagination


from rest_framework import filters as drf_filters
from rest_framework.views import APIView
import django_filters
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django.db.models.functions import Coalesce
from django.db.models import F, Sum, Q
from rest_framework.exceptions import ValidationError

from nxtbn.warehouse.utils import reserve_stock



class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    pagination_class = None


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

        # Query all warehouses and annotate stock data for the given variant
        warehouses = Warehouse.objects.annotate(
            total_quantity=Coalesce(
                Sum('stocks__quantity', filter=Q(stocks__product_variant=product_variant)), 
                0
            ),
            reserved_quantity=Coalesce(
                Sum('stocks__reserved', filter=Q(stocks__product_variant=product_variant)), 
                0
            )
        )

        # Prepare the response data
        data = []
        for warehouse in warehouses:
            available_quantity = warehouse.total_quantity - warehouse.reserved_quantity
            data.append({
                "warehouse_id": warehouse.id,
                "warehouse_name": warehouse.name,
                "quantity": warehouse.total_quantity,
                "reserved_quantity": warehouse.reserved_quantity,
                "available_quantity": available_quantity,
            })

        return Response(data, status=status.HTTP_200_OK)
    



class UpdateStockWarehouseWise(generics.UpdateAPIView):
    serializer_class = StockUpdateSerializer

    def update(self, request, *args, **kwargs):
        variant_id = kwargs.get('variant_id')
        payload = request.data 

        product_variant = get_object_or_404(ProductVariant, id=variant_id)

        for item in payload:
            warehouse_id = item.get("warehouse")
            quantity = int(item.get("quantity"))

            if quantity is None or quantity <= 0:
                # Skip if quantity is not provided or is <= 0
                continue

            warehouse = get_object_or_404(Warehouse, id=warehouse_id)

            try:
                # Check if the stock already exists
                stock = Stock.objects.get(warehouse=warehouse, product_variant=product_variant)
                stock.quantity = quantity  # Update the stock quantity
                stock.save()
            except Stock.DoesNotExist:
                # Create a new stock only if quantity > 0
                Stock.objects.create(warehouse=warehouse, product_variant=product_variant, quantity=quantity)

        return Response({"detail": "Stock updated successfully."}, status=status.HTTP_200_OK)
    

class StockReservationFilter(filters.FilterSet):
    warehouse = filters.CharFilter(field_name='stock__warehouse', lookup_expr='iexact')
    class Meta:
        model = StockReservation
        fields = [
            'id',
            'stock',
            'purpose',
            'warehouse',
        ]



class StockReservationFilterMixin:
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter
    ] 
    search_fields = [
        'id',
        'stock__product_variant__name',

    ]
    ordering_fields = [
        'quantity',
    ]
    filterset_class = StockReservationFilter

    def get_queryset(self):
        return StockReservation.objects.all()
    
class StockReservationListAPIView(StockReservationFilterMixin, generics.ListCreateAPIView):
    serializer_class = StockReservationSerializer
    queryset = StockReservation.objects.all()
    pagination_class = NxtbnPagination



class MergeStockReservationAPIView(generics.UpdateAPIView):
    """
    API to transfer stock reservation from one warehouse to another.
    """
    queryset = StockReservation.objects.all()
    serializer_class = MergeStockReservationSerializer

    def update(self, request, *args, **kwargs):
        reservation = self.get_object()
        serializer = self.get_serializer(reservation, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        destination_stock = serializer.validated_data['destination_stock']
        destination_reservation = serializer.validated_data.get('destination_reservation')

        # If a reservation already exists at the destination, merge it
        if destination_reservation:
            destination_reservation.quantity += reservation.quantity
            destination_reservation.save()

            # Adjust the reserved quantities of source and destination stocks
            source_stock = reservation.stock
            source_stock.reserved -= reservation.quantity
            source_stock.save()

            destination_stock.reserved += reservation.quantity
            destination_stock.save()

            # Delete the source reservation
            reservation.delete()
        else:
            # Update source stock reserved quantity
            source_stock = reservation.stock
            source_stock.reserved -= reservation.quantity
            source_stock.save()

            # Update destination stock reserved quantity
            destination_stock.reserved += reservation.quantity
            destination_stock.save()

            # Update reservation to point to destination stock
            reservation.stock = destination_stock
            reservation.save()

        return Response({"detail": "Stock reservation successfully transferred."}, status=status.HTTP_200_OK)


class RetryReservationAPIView(APIView):
    def post(self, request, alias):
        order = get_object_or_404(Order, alias=alias)
        reserve_stock(order)
        return Response({"detail": "Stock reservation retried successfully."}, status=status.HTTP_200_OK)
    


class StockTransferListCreateAPIView(generics.ListCreateAPIView):
    """List and create stock transfers"""
    queryset = StockTransfer.objects.prefetch_related('items').all()
    serializer_class = StockTransferSerializer
        