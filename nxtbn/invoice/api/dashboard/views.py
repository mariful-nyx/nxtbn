from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions  import AllowAny
from rest_framework.exceptions import APIException

from nxtbn.invoice.api.dashboard.serializers import OrderInvoiceSerializer
from nxtbn.order.models import Order


class OrderInvoiceAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderInvoiceSerializer
    lookup_field = 'alias'