from rest_framework import generics, viewsets
from nxtbn.purchase.api.dashboard.serializers import PurchaseOrderSerializer, PurchaseOrderDetailSerializer
from nxtbn.purchase.models import PurchaseOrder
from nxtbn.core.paginator import NxtbnPagination


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    pagination_class = NxtbnPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PurchaseOrderDetailSerializer
        return PurchaseOrderSerializer