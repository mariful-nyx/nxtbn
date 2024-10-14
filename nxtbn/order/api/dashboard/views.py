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
from dateutil.relativedelta import relativedelta
from django.db.models.functions import TruncMonth
import calendar

from decimal import Decimal

from rest_framework import filters as drf_filters
import django_filters
from django_filters import rest_framework as filters

from nxtbn.core.admin_permissions import NxtbnAdminPermission
from nxtbn.order.proccesor.views import OrderProccessorAPIView
from nxtbn.order import OrderAuthorizationStatus, OrderChargeStatus, OrderStatus
from nxtbn.order.models import Order, OrderLineItem
from nxtbn.payment import PaymentMethod
from nxtbn.payment.models import Payment
from nxtbn.product.models import ProductVariant
from nxtbn.users.admin import User
from nxtbn.filemanager.models import Image

from .serializers import CustomerCreateSerializer, OrderDetailsSerializer, OrderListSerializer, OrderSerializer, OrderStatusUpdateSerializer, OrderPaymentMethodSerializer, CustomerUpdateSerializer
from nxtbn.core.paginator import NxtbnPagination

from babel.numbers import get_currency_precision
import json



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
        today = timezone.now()
        last_week = today - timedelta(days=7)

        # Total Orders
        total_orders = Order.objects.count()
        orders_last_week = Order.objects.filter(created_at__gte=last_week).count()
        orders_last_week_percentage_change = (orders_last_week / total_orders) * 100 if total_orders > 0 else 0

        # Total Variants
        total_variants = ProductVariant.objects.count()

        # Total Sale (sum of total_price in Orders)
        total_sale = Order.objects.aggregate(total=Sum(F('total_price') / Decimal(100)))['total'] or Decimal(0)
        sales_last_week = Order.objects.filter(created_at__gte=last_week).aggregate(total=Sum(F('total_price') / Decimal(100)))['total'] or Decimal(0)
        sales_last_week_percentage_change = (sales_last_week / total_sale) * 100 if total_sale > 0 else 0

        # Net Sales (sum of payment_amount in Payments)
        net_sales = Payment.objects.aggregate(net_total=Sum(F('payment_amount') / Decimal(100)))['net_total'] or Decimal(0)
        net_sales_last_week = Payment.objects.filter(created_at__gte=last_week).aggregate(net_total=Sum(F('payment_amount') / Decimal(100)))['net_total'] or Decimal(0)
        net_sales_last_week_percentage_change = (net_sales_last_week / net_sales) * 100 if net_sales > 0 else 0


        # Total stock
        total_stock = ProductVariant.objects.filter(track_inventory=True).aggregate(total=Sum('stock'))['total'] or Decimal(0)
        total_untracked_stock = ProductVariant.objects.filter(track_inventory=False, stock_status='in_stock').count()

        net_stock = total_stock - OrderLineItem.objects.aggregate(total=Sum('quantity'))['total'] or 0
        
        backordered_stock = 0
        
        # Total Order
        total_orders = Order.objects.aggregate(total = Sum('total_price'))['total'] or Decimal(0)
        total_orders_last_week = Order.objects.filter(due_date__gte=last_week).aggregate(total=Sum('total_price'))['total'] or Decimal(0)
        total_orders_last_percentage_change = (total_orders_last_week/total_orders) * 100 
        
        # order processing
        order_processing = Order.objects.filter(status = 'PROCESSING').aggregate(total = Sum('total_price'))['total'] or Decimal(0)
        

        # order delivered
        order_delivered = Order.objects.filter(status = 'DELIVERED').aggregate(total = Sum('total_price'))['total'] or Decimal(0)
        
        last_order = Order.objects.latest('due_date')
        last_ordered_date = last_order.due_date if last_order else None

        #last five month sale graph
        five_months_ago = today - timedelta(days=30 * 5)  
        
        monthly_payments = (
            Payment.objects
            .filter(paid_at__gte=five_months_ago)
            .annotate(month=TruncMonth('paid_at')) 
            .values('month')
            .annotate(total=Sum('payment_amount'))  
            .order_by('month') 
        )
        
        results = {}
        
        for i in range(5):
            month_date = (today - timedelta(days=30 * i)).replace(day=1)
            results[month_date.strftime('%B %Y')] = 0 

        for payment in monthly_payments:
            month_key = payment['month'].strftime('%B %Y')
            results[month_key] = payment['total']

        
        # Calculate most selling product 
        most_selling_product = []

        most_selling_variants = (
            ProductVariant.objects
            .annotate(total_sold=Sum('orderlineitems__quantity'))
            .order_by('-total_sold')  # Order by total sold in descending order
        )


        for variant in most_selling_variants:
            name = variant.name
     
            most_selling_product.append({
                'name': f"{variant.product.name}-{name}",
                'image': request.build_absolute_uri(variant.variant_image.image.url if variant.variant_image and variant.variant_image.image else None),
                'sales': variant.total_sold,
                'stock': variant.stock,
                'price': variant.price
            })

     
        data = {
            'sales': {
                'amount': total_sale,
                'last_percentage_change': sales_last_week_percentage_change
            },
            'orders': {
                'amount': total_orders,
                'last_percentage_change': orders_last_week_percentage_change
            },
            'variants': {
                'amount': total_variants,
            },
            'net_sales': {
                'amount': net_sales,
                'last_percentage_change': net_sales_last_week_percentage_change
            },
            'total_stock': {
                'amount': total_stock
            },
            'total_untracked_stock': {
                'amount': total_untracked_stock
            },
            'net_stock' : {
                'amount': net_stock
            },
            'backordered_stock':{
                'amount': 0
            },
            'total_order': {
                'amount': total_orders,
                'last_percentage_change': 0,
                'last_ordered_date': last_ordered_date,
            },
            'order_processing': {
                'amount': order_processing,
                'last_percentage_change': 0
            },
            'order_delivered': {
                'amount': order_delivered,
                'last_percentage_change': 0
            },
            'sell_past_month': {
                'results': results
            },
            'most_selling_product': {
                'results': most_selling_product
            }
        }
        
        return Response(data)
    

class OrderEastimateView(OrderProccessorAPIView):
    create_order = False # Eastimate order

class OrderCreateView(OrderProccessorAPIView):
    create_order = True # Eastimate and create order

class CreateCustomAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerCreateSerializer

class UpdateCustomAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerUpdateSerializer
    lookup_field = 'id'

class OrderStatusUpdateAPIView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    lookup_field = 'alias'

class OrderPaymentMethodUpdateAPIView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderPaymentMethodSerializer
    lookup_field = 'alias'