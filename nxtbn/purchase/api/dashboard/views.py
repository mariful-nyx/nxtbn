from rest_framework import generics, viewsets, status
from nxtbn.purchase.api.dashboard.serializers import InventoryReceivingSerializer, PurchaseOrderCreateSerializer, PurchaseOrderSerializer, PurchaseOrderDetailSerializer
from nxtbn.purchase.models import PurchaseOrder, PurchaseOrderItem
from django.db import transaction
from nxtbn.core.paginator import NxtbnPagination
from nxtbn.warehouse.models import Stock


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    pagination_class = NxtbnPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PurchaseOrderCreateSerializer
        if self.action == "retrieve":
            return PurchaseOrderDetailSerializer
        
        return PurchaseOrderSerializer
    
    from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from nxtbn.purchase.api.dashboard.serializers import (
    PurchaseOrderCreateSerializer, 
    PurchaseOrderSerializer, 
    PurchaseOrderDetailSerializer
)
from nxtbn.purchase.models import PurchaseOrder
from nxtbn.core.paginator import NxtbnPagination
from nxtbn.purchase import PurchaseStatus


from django.db import transaction
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    pagination_class = NxtbnPagination

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != PurchaseStatus.DRAFT:
            return Response({
                "error": "Only purchase orders with status 'DRAFT' can be deleted."
            }, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            self.perform_destroy(instance)
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PurchaseOrderCreateSerializer
        if self.action == "retrieve":
            return PurchaseOrderDetailSerializer
        
        return PurchaseOrderSerializer

    @action(detail=True, methods=['patch'], url_path='mark-as-ordered')
    def mark_as_ordered(self, request, pk=None):
        """Marks the purchase order as ordered."""
        try:
            with transaction.atomic():
                purchase_order = self.get_object()
                
                if purchase_order.status in [PurchaseStatus.RECEIVED_AND_CLOSED, PurchaseStatus.CANCELLED]:
                    return Response({
                        "error": "Purchase order is already received or cancelled."
                    }, status=status.HTTP_400_BAD_REQUEST)

                purchase_order.status = PurchaseStatus.PENDING
                purchase_order.save()

                # Update stock levels as incoming stock with associated warehouse
                for item in purchase_order.items.all():
                    stock, created = Stock.objects.get_or_create(
                        warehouse=purchase_order.destination,
                        defaults={'incoming': item.ordered_quantity},
                        product_variant=item.variant,
                    )
                    if not created:
                        stock.incoming += item.ordered_quantity
                        stock.save()

            return Response({
                "message": "Purchase order marked as ordered successfully.",
                "purchase_order": PurchaseOrderSerializer(purchase_order).data
            }, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response({
                "error": "Purchase order not found."
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "error": "An error occurred while marking the purchase order as ordered."
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], url_path='cancel')
    def cancel(self, request, pk=None):
        """Cancels the purchase order."""
        try:
            with transaction.atomic():
                purchase_order = self.get_object()
                
                if purchase_order.status in [PurchaseStatus.RECEIVED, PurchaseStatus.CANCELLED, PurchaseStatus.PENDING]:
                    return Response({
                        "error": "Purchase order is already received, cancelled, or marked as ordered."
                    }, status=status.HTTP_400_BAD_REQUEST)

                purchase_order.status = PurchaseStatus.CANCELLED
                purchase_order.save()

            return Response({
                "message": "Purchase order cancelled successfully.",
                "purchase_order": PurchaseOrderSerializer(purchase_order).data
            }, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response({
                "error": "Purchase order not found."
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "error": "An error occurred while cancelling the purchase order."
            }, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['patch'], url_path='mark-as-received')
    def mark_as_received(self, request, pk=None):
        """
            When we receive it, it will be marked as received and the stock levels will be updated.
            Incoming stock will be reduced and quantity will be increased based on the received quantity.
            After marking as received, the purchase order will be closed and no further changes can be made.
        """
        try:
            with transaction.atomic():
                purchase_order = self.get_object()
                
                if purchase_order.status != PurchaseStatus.PENDING:
                    return Response({
                        "error": "Only purchase orders with status 'PENDING' can be marked as received."
                    }, status=status.HTTP_400_BAD_REQUEST)

                purchase_order.status = PurchaseStatus.RECEIVED_AND_CLOSED
                purchase_order.save()

                # Update stock levels as received stock with associated warehouse
                for item in purchase_order.items.all():
                    stock = Stock.objects.get(warehouse=purchase_order.destination, product_variant=item.variant)
                    stock.incoming -= item.ordered_quantity
                    stock.quantity += item.received_quantity
                    stock.save()

            return Response({
                "message": "Purchase order marked as received successfully.",
                "purchase_order": PurchaseOrderSerializer(purchase_order).data
            }, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response({
                "error": "Purchase order not found."
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "error": "An error occurred while marking the purchase order as received."
            }, status=status.HTTP_400_BAD_REQUEST)

        

class InventoryReceivingAPI(generics.UpdateAPIView):
    serializer_class = InventoryReceivingSerializer
    lookup_field = 'pk'
    queryset = PurchaseOrder.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.status != PurchaseStatus.PENDING:
            return Response(
                {"error": "Only purchase orders with status 'PENDING' can be received."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data, context={'instance': instance})
        serializer.is_valid(raise_exception=True)

        items_data = serializer.validated_data['items']

        with transaction.atomic():
            for item_data in items_data:
                item_id = item_data['id']
                received_quantity = item_data['received_quantity']
                rejected_quantity = item_data['rejected_quantity']

                try:
                    order_item = instance.items.get(id=item_id)
                    order_item.received_quantity = received_quantity
                    order_item.rejected_quantity = rejected_quantity
                    order_item.save()
                except PurchaseOrderItem.DoesNotExist:
                    raise serializers.ValidationError(f"Item with id {item_id} does not exist in the purchase order.")
                except Stock.DoesNotExist:
                    raise serializers.ValidationError(f"Stock entry not found for item id {item_id}.")

        return Response({"message": "Inventory receiving updated successfully."}, status=status.HTTP_200_OK)