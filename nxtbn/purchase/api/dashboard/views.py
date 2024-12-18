from rest_framework import generics, viewsets
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

        
