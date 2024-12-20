from rest_framework import generics, viewsets, status
from nxtbn.purchase.api.dashboard.serializers import PurchaseOrderCreateSerializer, PurchaseOrderSerializer, PurchaseOrderDetailSerializer
from nxtbn.purchase.models import PurchaseOrder
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
        
