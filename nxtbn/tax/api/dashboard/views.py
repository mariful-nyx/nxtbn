from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions  import AllowAny
from rest_framework.exceptions import APIException

from nxtbn.core.paginator import NxtbnPagination
from nxtbn.core.admin_permissions import NxtbnAdminPermission

from nxtbn.tax.models import TaxClass, TaxRate
from nxtbn.tax.api.dashboard.serializers import (
    TaxClassSerializer, 
    TaxClassCreateSerializer, 
    TaxClassUpdateSerializer,
    TaxClassDetailSerializer, 
    TaxRateSerializer
    
    )


class TaxClassView(generics.ListCreateAPIView):
    permission_classes = (NxtbnAdminPermission,)
    queryset = TaxClass.objects.all()
    serializer_class = TaxClassSerializer
    pagination_class = NxtbnPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaxClassCreateSerializer
        return TaxClassSerializer


class TaxClassRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (NxtbnAdminPermission,)
    queryset = TaxClass.objects.all()
    serializer_class = TaxClassDetailSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return TaxClassUpdateSerializer
        return TaxClassDetailSerializer

