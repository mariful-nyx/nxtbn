
from django.db.models import Q
from nxtbn.order import AddressType
from nxtbn.shipping.api.dashboard.serializers import ShippingMethodSerializer
from nxtbn.shipping.models import ShippingMethod, ShippingRate
from rest_framework import generics
from rest_framework.response import Response

from nxtbn.users.models import User

class CustomerEligibleShippingMethodstAPI(generics.ListAPIView):
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