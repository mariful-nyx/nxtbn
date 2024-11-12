from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions  import AllowAny
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from django.db.models import Sum, Count, F
from django.utils import timezone

from datetime import timedelta

from decimal import Decimal

from rest_framework import filters as drf_filters
import django_filters
from django_filters import rest_framework as filters

from nxtbn.core.admin_permissions import NxtbnAdminPermission
from nxtbn.core.utils import to_currency_unit
from nxtbn.order.proccesor.views import OrderProccessorAPIView
from nxtbn.order import OrderAuthorizationStatus, OrderChargeStatus, OrderStatus, ReturnStatus
from nxtbn.order.models import Order, OrderLineItem, ReturnLineItem, ReturnRequest
from nxtbn.payment import PaymentMethod
from nxtbn.payment.models import Payment
from nxtbn.product.models import ProductVariant
from nxtbn.users.admin import User
from .serializers import CustomerCreateSerializer, OrderDetailsSerializer, OrderListSerializer, OrderPaymentUpdateSerializer, OrderStatusUpdateSerializer, OrderPaymentMethodSerializer, ReturnLineItemSerializer, ReturnLineItemStatusUpdateSerializer, ReturnRequestBulkUpdateSerializer, ReturnRequestDetailsSerializer, ReturnRequestSerializer, ReturnRequestStatusUpdateSerializer
from nxtbn.core.paginator import NxtbnPagination
from datetime import datetime

from babel.numbers import get_currency_precision



class OrderFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=OrderStatus.choices)
    charge_status = filters.ChoiceFilter(choices=OrderChargeStatus.choices)
    authorize_status = filters.ChoiceFilter(choices=OrderAuthorizationStatus.choices)
    currency = filters.CharFilter(field_name='currency', lookup_expr='iexact')
    payment_method = django_filters.ChoiceFilter(choices=PaymentMethod.choices, method='filter_by_payment_method')
    created_at = filters.DateFromToRangeFilter(field_name='created_at') # eg. ?created_at_after=2023-09-01&created_at_before=2023-09-12
    min_order_value = django_filters.NumberFilter(field_name='total_price', lookup_expr='gte', method='filter_min_order_value')
    max_order_value = django_filters.NumberFilter(field_name='total_price', lookup_expr='lte', method='filter_max_order_value')

    class Meta:
        model = Order
        fields = [
            'status',
            'charge_status',
            'authorize_status',
            'currency',
            'payment_method',
            'created_at',
            'min_order_value',
            'max_order_value',
        ]

    def filter_by_payment_method(self, queryset, name, value):
        return queryset.filter(payments__payment_method=value).distinct()
    
    def filter_min_order_value(self, queryset, name, value):
        """
        Filter orders with total_price greater than or equal to the specified min_order_value in units.
        """
        if value is not None:
            precision = get_currency_precision(settings.BASE_CURRENCY)
            min_value_in_subunits = int(value * (10 ** precision))
            return queryset.filter(total_price__gte=min_value_in_subunits)
        return queryset

    def filter_max_order_value(self, queryset, name, value):
        """
        Filter orders with total_price less than or equal to the specified max_order_value in units.
        """
        if value is not None:
            precision = get_currency_precision(settings.BASE_CURRENCY)
            max_value_in_subunits = int(value * (10 ** precision))
            return queryset.filter(total_price__lte=max_value_in_subunits)
        return queryset


class OrderListView(generics.ListAPIView):
    permission_classes = (NxtbnAdminPermission,)
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    pagination_class = NxtbnPagination

    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter
    ]
    filterset_class = OrderFilter
    search_fields = ['alias', 'id', 'user__username', 'supplier__name']
    ordering_fields = ['created_at']


class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = (NxtbnAdminPermission,)
    queryset = Order.objects.all()
    serializer_class = OrderDetailsSerializer
    lookup_field = 'alias'


class BasicStatsView(APIView):

    def get(self, request):
        # Get start and end dates from query parameters
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        range_name = request.query_params.get('range_name', None)

        # Parse dates if provided, or default to all-time if not provided
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else None
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d") + timedelta(days=1) if end_date_str else timezone.now() + timedelta(days=1) # Add 1 day to adjust for end date as inclusive


        # Set a previous period for calculating percentage change
        if start_date and end_date:
            previous_start_date = start_date - (end_date - start_date)
            previous_end_date = start_date
        else:
            previous_end_date = end_date - timedelta(days=7)
            previous_start_date = previous_end_date - timedelta(days=7)

        # Filter current period orders
        orders_queryset = Order.objects.all()
        if start_date:
            orders_queryset = orders_queryset.filter(created_at__gte=start_date)
        if end_date:
            orders_queryset = orders_queryset.filter(created_at__lte=end_date)

        # Total Orders
        total_orders = orders_queryset.count()

        # Total Sale (sum of total_price in Orders)
        total_sale = orders_queryset.aggregate(total=Sum(F('total_price')))['total'] or 0

        # Net Sales (sum of payment_amount in Payments, filtered by the same date range)
        payments_queryset = Payment.objects.all()
        if start_date:
            payments_queryset = payments_queryset.filter(created_at__gte=start_date)
        if end_date:
            payments_queryset = payments_queryset.filter(created_at__lte=end_date)

        net_sales = payments_queryset.aggregate(net_total=Sum(F('payment_amount')))['net_total'] or 0
        total_variants = ProductVariant.objects.count()

        data = {
            'percetage_change_preiod_title': '',
            'sales': {
                'amount': to_currency_unit(total_sale, settings.BASE_CURRENCY, locale='en_US'),
                'last_percentage_change': ''
            },
            'orders': {
                'amount': total_orders,
                'last_percentage_change': ''
            },
            'variants': {
                'amount': total_variants,
            },
            'net_sales': {
                'amount': to_currency_unit(net_sales, settings.BASE_CURRENCY, locale='en_US'),
                'last_percentage_change': ''
            }
        }

        comparables = ['today', 'this week', 'this month', 'this year',]

        # Calculate totals for the previous period
        if range_name and  range_name.lower() in comparables:
            previous_orders_queryset = Order.objects.filter(created_at__gte=previous_start_date, created_at__lte=previous_end_date)
            previous_total_orders = previous_orders_queryset.count()
            previous_total_sale = previous_orders_queryset.aggregate(total=Sum(F('total_price')))['total'] or 0

            previous_payments_queryset = Payment.objects.filter(created_at__gte=previous_start_date, created_at__lte=previous_end_date)
            previous_net_sales = previous_payments_queryset.aggregate(net_total=Sum(F('payment_amount')))['net_total'] or 0

            # Calculate percentage changes
            orders_last_percentage_change = round(((total_orders - previous_total_orders) / previous_total_orders * 100), 2) if previous_total_orders > 0 else 0
            sales_last_percentage_change = round(((total_sale - previous_total_sale) / previous_total_sale * 100), 2) if previous_total_sale > 0 else 0
            net_sales_last_percentage_change = round(((net_sales - previous_net_sales) / previous_net_sales * 100), 2) if previous_net_sales > 0 else 0

            data['sales']['last_percentage_change'] = sales_last_percentage_change
            data['orders']['last_percentage_change'] = orders_last_percentage_change
            data['net_sales']['last_percentage_change'] = net_sales_last_percentage_change


            compare_title = {
                'today': _('Yesterday'),
                'this week': _('Last Week'),
                'this month': _('Last Month'),
                'this year': _('Last Year'),
            }
            data['percetage_change_preiod_title'] = compare_title[range_name.lower()]
        

        return Response(data)
    

class OrderEastimateView(OrderProccessorAPIView):
    create_order = False # Eastimate order

class OrderCreateView(OrderProccessorAPIView):
    create_order = True # Eastimate and create order

class CreateCustomAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerCreateSerializer

class OrderStatusUpdateAPIView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    lookup_field = 'alias'

class OrderPaymentTermUpdateAPIView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderPaymentUpdateSerializer
    lookup_field = 'alias'
class OrderPaymentMethodUpdateAPIView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderPaymentMethodSerializer
    lookup_field = 'alias'


class ReturnRequestAPIView(generics.ListCreateAPIView):
    queryset = ReturnRequest.objects.all()
    serializer_class = ReturnRequestSerializer
    
class ReturnRequestDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = ReturnRequest.objects.all()
    serializer_class = ReturnRequestDetailsSerializer
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return ReturnRequestStatusUpdateSerializer
        return self.serializer_class

class ReturnLineItemStatusUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ReturnLineItemStatusUpdateSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        receiving_status = serializer.validated_data['receiving_status']
        line_item_ids = serializer.validated_data['line_item_ids']

        # Update the receiving status for the specified line items
        line_items = ReturnLineItem.objects.filter(id__in=line_item_ids)

        if line_items.count() != len(line_item_ids):
            return Response(
                {"error": "Some line items were not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        line_items.update(receiving_status=receiving_status)

        return Response(
            {"message": "Receiving status updated successfully."},
            status=status.HTTP_200_OK
        )
    

class ReturnRequestBulkUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ReturnRequestBulkUpdateSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_ids = serializer.validated_data['request_ids']
        request_status = serializer.validated_data['status']

        # Update the status for the specified return requests
        return_requests = ReturnRequest.objects.filter(id__in=request_ids)

        to_update = {
            'status': request_status
        }

        if request_status == ReturnStatus.APPROVED:
            to_update['approved_at'] = timezone.now()
            to_update['approved_by'] = request.user

        if request_status == ReturnStatus.REVIEWED:
            to_update['reviewed_by'] = request.user

        if request_status == ReturnStatus.COMPLETED:
            to_update['completed_at'] = timezone.now()
            to_update['completed_by'] = request.user

        if request_status == ReturnStatus.CANCELLED:
            to_update['cancelled_at'] = timezone.now()

        return_requests.update(**to_update)

        return Response(
            {"message": "Return requests updated successfully."},
            status=status.HTTP_200_OK
        )