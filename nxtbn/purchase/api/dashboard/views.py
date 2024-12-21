from rest_framework import generics, viewsets, status
from nxtbn.purchase.api.dashboard.serializers import InventoryReceivingSerializer, PurchaseOrderCreateSerializer, PurchaseOrderSerializer, PurchaseOrderDetailSerializer
from nxtbn.purchase.models import PurchaseOrder, PurchaseOrderItem
from nxtbn.core.paginator import NxtbnPagination


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
            purchase_order = self.get_object()
            
            if purchase_order.status in [PurchaseStatus.RECEIVED, PurchaseStatus.CANCELLED]:
                return Response({
                    "error": "Purchase order is already received or cancelled."
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                purchase_order.status = PurchaseStatus.PENDING
                purchase_order.save()

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
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], url_path='cancel')
    def cancel(self, request, pk=None):
        """Cancels the purchase order."""
        try:
            purchase_order = self.get_object()
            
            if purchase_order.status in [PurchaseStatus.RECEIVED, PurchaseStatus.CANCELLED, PurchaseStatus.PENDING]:
                return Response({
                    "error": "Purchase order is already received, cancelled or marked as ordered."
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
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
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        

class InventoryReceivingAPI(generics.UpdateAPIView):
    serializer_class = InventoryReceivingSerializer
    lookup_field = 'pk'
    queryset = PurchaseOrder.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'instance': instance})
        serializer.is_valid(raise_exception=True)

        items_data = serializer.validated_data['items']
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
                return Response(
                    {"error": f"Item with id {item_id} does not exist in the purchase order."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response({"message": "Inventory receiving updated successfully."}, status=status.HTTP_200_OK)