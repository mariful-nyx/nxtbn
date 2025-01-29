from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from nxtbn.core.admin_permissions import RoleBasedHTTPMethodPermission
from nxtbn.core.paginator import NxtbnPagination
from nxtbn.discount.models import PromoCode, PromoCodeCustomer, PromoCodeProduct, PromoCodeUsage
from nxtbn.discount.api.dashboard.serializers import AttachPromoCodeEntitiesSerializer, PromoCodeCustomerSerializer, PromoCodeProductSerializer, PromoCodeCountedSerializer, PromoCodeUsageSerializer

from rest_framework import filters as drf_filters
import django_filters
from django_filters import rest_framework as filters

from nxtbn.users import UserRole


class PromocodeFilter(filters.FilterSet):
    username = filters.CharFilter(field_name='username', lookup_expr='icontains')
    date_joined = filters.DateFromToRangeFilter(field_name='date_joined')
    expiration_date = filters.DateFromToRangeFilter(field_name='expiration_date')

    class Meta:
        model = PromoCode
        fields = [
            'id',
            'code',
            'value',
            'expiration_date',
            'is_active',
        ]


class PromocodeFilterMixin:
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter
    ] 
    search_fields = [
        'id',
        'code',
        'value',

    ]
    ordering_fields = [
        'code',
        'expiration_date',
    ]
    filterset_class = PromocodeFilter

    def get_queryset(self):
        return PromoCode.objects.all()
    
class PromoCodeListCreateAPIView(PromocodeFilterMixin, generics.ListCreateAPIView):
    pagination_class = NxtbnPagination
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeCountedSerializer

    permission_classes = (RoleBasedHTTPMethodPermission,)
    HTTP_PERMISSIONS = {
        UserRole.STORE_MANAGER: {"all"},
        UserRole.ADMIN: {"all"},
        UserRole.PRODUCT_MANAGER: {"get"},
        UserRole.ORDER_PROCESSOR: {"get"},
        UserRole.STORE_VIEWER: {"get"},
        UserRole.ACCOUNTANT: {"get"},
        UserRole.MARKETING_MANAGER: {"get"},
    }


class PromoCodeUpdateRetrieveDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeCountedSerializer
    lookup_field = 'id'

    permission_classes = (RoleBasedHTTPMethodPermission,)
    HTTP_PERMISSIONS = {
        UserRole.STORE_MANAGER: {"all"},
        UserRole.ADMIN: {"all"},
        UserRole.PRODUCT_MANAGER: {"get"},
        UserRole.ORDER_PROCESSOR: {"get"},
        UserRole.STORE_VIEWER: {"get"},
        UserRole.ACCOUNTANT: {"get"},
        UserRole.MARKETING_MANAGER: {"get"},
    }

class AttachPromoCodeEntitiesAPIView(generics.CreateAPIView):
    serializer_class = AttachPromoCodeEntitiesSerializer

    permission_classes = (RoleBasedHTTPMethodPermission,)
    HTTP_PERMISSIONS = {
        UserRole.STORE_MANAGER: {"all"},
        UserRole.ADMIN: {"all"},
        UserRole.PRODUCT_MANAGER: {"get"},
        UserRole.ORDER_PROCESSOR: {"get"},
        UserRole.STORE_VIEWER: {"get"},
        UserRole.ACCOUNTANT: {"get"},
        UserRole.MARKETING_MANAGER: {"get"},
    }

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

    permission_classes = (RoleBasedHTTPMethodPermission,)
    HTTP_PERMISSIONS = {
        UserRole.STORE_MANAGER: {"all"},
        UserRole.ADMIN: {"all"},
        UserRole.PRODUCT_MANAGER: {"get"},
        UserRole.ORDER_PROCESSOR: {"get"},
        UserRole.STORE_VIEWER: {"get"},
        UserRole.ACCOUNTANT: {"get"},
        UserRole.MARKETING_MANAGER: {"get"},
    }


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

    permission_classes = (RoleBasedHTTPMethodPermission,)
    HTTP_PERMISSIONS = {
        UserRole.STORE_MANAGER: {"all"},
        UserRole.ADMIN: {"all"},
        UserRole.PRODUCT_MANAGER: {"get"},
        UserRole.ORDER_PROCESSOR: {"get"},
        UserRole.STORE_VIEWER: {"get"},
        UserRole.ACCOUNTANT: {"get"},
        UserRole.MARKETING_MANAGER: {"get"},
    }




class PromoCodeUsageListAPIView(generics.ListAPIView):
    queryset = PromoCodeUsage.objects.all()
    serializer_class = PromoCodeUsageSerializer
    pagination_class = NxtbnPagination

    permission_classes = (RoleBasedHTTPMethodPermission,)
    HTTP_PERMISSIONS = {
        UserRole.STORE_MANAGER: {"all"},
        UserRole.ADMIN: {"all"},
        UserRole.PRODUCT_MANAGER: {"get"},
        UserRole.ORDER_PROCESSOR: {"get"},
        UserRole.STORE_VIEWER: {"get"},
        UserRole.ACCOUNTANT: {"get"},
        UserRole.MARKETING_MANAGER: {"get"},
    }

