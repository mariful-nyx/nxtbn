from rest_framework import generics
from nxtbn.purchase.api.dashboard.serializers import PurchaseOrderSerializer
from nxtbn.purchase.models import PurchaseOrder
from nxtbn.core.paginator import NxtbnPagination


class PurchaseOrderList(generics.ListAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    pagination_class = NxtbnPagination