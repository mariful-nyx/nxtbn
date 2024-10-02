
from django.db.models import Q
from nxtbn.order import AddressType
from nxtbn.shipping.api.dashboard.serializers import (
    ShippingMethodSerializer, 
    ShppingMethodDetailSeralizer,
    ShippingRateSerializer
)
from nxtbn.shipping.models import ShippingMethod, ShippingRate
from rest_framework import generics
from rest_framework.response import Response

from nxtbn.users.models import User

class CustomerEligibleShippingMethodstAPI(generics.ListCreateAPIView):
    serializer_class = ShippingMethodSerializer

    def get_queryset(self):
        country = self.request.query_params.get('country')
        region = self.request.query_params.get('region')
        city = self.request.query_params.get('city')

        # Start by getting all ShippingMethods
        queryset = ShippingMethod.objects.all()

        # Filter ShippingMethods based on related ShippingRate location data
        if country or region or city:
            queryset = queryset.filter(
                rates__in=ShippingRate.objects.filter(
                    Q(country__iexact=country) | Q(country__isnull=True),
                    Q(region__iexact=region) | Q(region__isnull=True),
                    Q(city__iexact=city) | Q(city__isnull=True)
                )
            ).distinct()

        return queryset


class CustomerEligibleShippingMethodDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ShppingMethodDetailSeralizer
    queryset = ShippingMethod.objects.all()
    lookup_field = 'id'


class ShippingRateView(generics.ListCreateAPIView):
    serializer_class = ShippingRateSerializer

    def get_queryset(self):
        shipping_method_id = self.kwargs['shipping_method_id']
        return ShippingRate.objects.filter(shipping_method_id=shipping_method_id)
    
    def perform_create(self, serializer):
        shipping_method = ShippingMethod.objects.get(id=self.kwargs['shipping_method_id'])
        serializer.save(shipping_method=shipping_method)


class ShippingRateDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ShippingRateSerializer
    queryset = ShippingRate.objects.all()
    lookup_field = 'id'