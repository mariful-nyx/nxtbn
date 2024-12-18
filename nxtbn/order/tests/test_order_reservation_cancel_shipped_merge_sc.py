import random
from decimal import Decimal
from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse
from nxtbn.core import PublishableStatus
from nxtbn.core.utils import normalize_amount_currencywise
from nxtbn.home.base_tests import BaseTestCase
from nxtbn.order import OrderStatus
from nxtbn.product.models import Product, ProductVariant
from rest_framework.test import APIClient
from nxtbn.product.tests import ProductFactory, ProductTypeFactory, ProductVariantFactory
from nxtbn.shipping.tests import ShippingMethodFactory
from nxtbn.tax.tests import TaxClassFactory, TaxRateFactory
from nxtbn.warehouse.tests import StockFactory, WarehouseFactory

from django.test.utils import override_settings
from django.db.models import Sum


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class OrderStockReservationTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.adminLogin()

        self.product_type = ProductTypeFactory(
            name="Physical Product Type",
        )


        self.variant = ProductVariantFactory(
            product=ProductFactory(
                product_type=self.product_type,
                status=PublishableStatus.PUBLISHED,
            ),
            track_inventory=True,
            allow_backorder=False   ,
            currency=settings.BASE_CURRENCY,
            price=normalize_amount_currencywise(100.00, settings.BASE_CURRENCY),
            cost_per_unit=50.00,
        )   
        

        self.warehosue_us_central= WarehouseFactory()
        self.warehosue_us_east= WarehouseFactory()
        self.warehosue_us_west= WarehouseFactory()
        

        StockFactory(
            warehouse=self.warehosue_us_central,
            product_variant=self.variant,
            quantity=5,
            reserved=0,
        )

        StockFactory(
            warehouse=self.warehosue_us_east,
            product_variant=self.variant,
            quantity=6,
            reserved=0,
        )
       



        self.order_api_url = reverse('admin_order_create')
        self.order_estimate_api_url = reverse('admin_order_estimate')

    def test_order_stock_tracking_with_disallowed_backorder(self):
        
        payload_more_than_stock = {
            "variants": [
                {
                    "alias": self.variant.alias,
                    "quantity": 15, # Expect bad request as we have only 11 quantity in stock
                },
            ]
        }

        order_out_of_stock_response_with_stock_tracking = self.auth_client.post(self.order_api_url, payload_more_than_stock, format='json')
        self.assertEqual(order_out_of_stock_response_with_stock_tracking.status_code, status.HTTP_400_BAD_REQUEST)


        payload_less_than_stock = {
                "variants": [
                    {
                        "alias": self.variant.alias,
                        "quantity": 7, # Expect success as we have 11 quantity in stock
                    },
                ]
            }

        order_less_than_stock_response_with_stock_tracking = self.auth_client.post(self.order_api_url, payload_less_than_stock, format='json')
        self.assertEqual(order_less_than_stock_response_with_stock_tracking.status_code, status.HTTP_200_OK)

        # as order is successfully created, we should have 7 reserved quantity of 11 quantity in stock
        remained_stock = ProductVariant.objects.get(alias=self.variant.alias).warehouse_stocks.aggregate(total=Sum('quantity'))['total']
        reserved_stock = ProductVariant.objects.get(alias=self.variant.alias).warehouse_stocks.aggregate(total=Sum('reserved'))['total']

        self.assertEqual(remained_stock, 11)
        self.assertEqual(reserved_stock, 7)


        # Now Ship the successfull order
        order_status_update_url = reverse('order-status-update', args=[order_less_than_stock_response_with_stock_tracking.data['order_alias']])
        approve = self.auth_client.patch(order_status_update_url, {"status": OrderStatus.APPROVED}, format='json')
        processing = self.auth_client.patch(order_status_update_url, {"status": OrderStatus.PROCESSING}, format='json')
        approved = self.auth_client.patch(order_status_update_url, {"status": OrderStatus.SHIPPED}, format='json')

        self.assertEqual(approve.status_code, status.HTTP_200_OK)
        self.assertEqual(processing.status_code, status.HTTP_200_OK)
        self.assertEqual(approved.status_code, status.HTTP_200_OK)

        # as it is shipped, reserved quantity should be 0 and stock should be 4
        remained_stock_after_shipping = ProductVariant.objects.get(alias=self.variant.alias).warehouse_stocks.aggregate(total=Sum('quantity'))['total']
        reserved_stock_after_shipping = ProductVariant.objects.get(alias=self.variant.alias).warehouse_stocks.aggregate(total=Sum('reserved'))['total']

        self.assertEqual(remained_stock_after_shipping, 4)
        self.assertEqual(reserved_stock_after_shipping, 0)

        # TODO: Implement return request and return line item status update test cases