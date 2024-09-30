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
    TaxClassDetailSerializer, 
    TaxRateSerializer
    
    )


class TaxClassView(generics.ListCreateAPIView):
    permission_classes = (NxtbnAdminPermission,)
    queryset = TaxClass.objects.all()
    serializer_class = TaxClassSerializer
    pagination_class = NxtbnPagination


class TaxClassRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (NxtbnAdminPermission,)
    queryset = TaxClass.objects.all()
    serializer_class = TaxClassDetailSerializer
    lookup_field = 'id'


class TaxRateListByTaxClass(generics.ListCreateAPIView):
    serializer_class = TaxRateSerializer

    def get_queryset(self):
        tax_class_id = self.kwargs['tax_class_id']
        return TaxRate.objects.filter(tax_class_id=tax_class_id)
    
    def perform_create(self, serializer):
        tax_class = TaxClass.objects.get(id=self.kwargs['tax_class_id'])
        serializer.save(tax_class=tax_class)
    

class TaxRateRetrieveUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaxRateSerializer
    queryset = TaxRate.objects.all()
    lookup_field = 'id'




        