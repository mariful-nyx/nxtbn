from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from nxtbn.core.paginator import NxtbnPagination
from nxtbn.discount.models import PromoCode, PromoCodeCustomer, PromoCodeProduct, PromoCodeUsage
from nxtbn.discount.api.dashboard.serializers import AttachPromoCodeEntitiesSerializer, PromoCodeCustomerSerializer, PromoCodeProductSerializer, PromoCodeCountedSerializer, PromoCodeUsageSerializer

from rest_framework import filters as drf_filters
import django_filters
from django_filters import rest_framework as filters

class PromoCodeListCreateAPIView(generics.ListCreateAPIView):
    pagination_class = NxtbnPagination
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeCountedSerializer


class PromoCodeUpdateRetrieveDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeCountedSerializer
    lookup_field = 'id'

class AttachPromoCodeEntitiesAPIView(generics.CreateAPIView):
    serializer_class = AttachPromoCodeEntitiesSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        promo_code = serializer.save()

        return Response(
            {"detail": f"Successfully attached entities to Promo Code '{promo_code.code}'."},
            status=status.HTTP_200_OK
        )

class PromoCodeProductFilter(filters.FilterSet):
    promo_code = filters.CharFilter(field_name='promo_code__code', lookup_expr='exact')

    class Meta:
        model = PromoCodeProduct
        fields = ['promo_code']
class PromoCodeProductListAPIView(generics.ListAPIView):
    queryset = PromoCodeProduct.objects.all()
    serializer_class = PromoCodeProductSerializer
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        # drf_filters.SearchFilter,
        # drf_filters.OrderingFilter
    ]
    filterset_class = PromoCodeProductFilter


class PromoCodeCustomerFilter(filters.FilterSet):
    promo_code = filters.CharFilter(field_name='promo_code__code', lookup_expr='exact')

    class Meta:
        model = PromoCodeCustomer
        fields = ['promo_code']
class PromoCodeCustomertListAPIView(generics.ListAPIView):
    queryset = PromoCodeCustomer.objects.all()
    serializer_class = PromoCodeCustomerSerializer
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        # drf_filters.SearchFilter,
        # drf_filters.OrderingFilter
    ]
    filterset_class = PromoCodeCustomerFilter




class PromoCodeUsageListAPIView(generics.ListAPIView):
    queryset = PromoCodeUsage.objects.all()
    serializer_class = PromoCodeUsageSerializer
