import random
from decimal import Decimal
from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse
from nxtbn.core import PublishableStatus
from nxtbn.core.utils import normalize_amount_currencywise
from nxtbn.home.base_tests import BaseTestCase
from nxtbn.product.models import Product
from rest_framework.test import APIClient
from nxtbn.product.tests import ProductFactory, ProductTypeFactory, ProductVariantFactory
from nxtbn.shipping.tests import ShippingMethodFactory
from nxtbn.tax.tests import TaxClassFactory, TaxRateFactory
from nxtbn.warehouse.tests import WarehouseFactory

from django.test.utils import override_settings


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class OrderStockReservationTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.adminLogin()

        self.country = 'US'
        self.state = 'NY'

       

        self.product_type = ProductTypeFactory(
            name="Physical Product Type",
            track_stock=True,
            taxable=True,
            physical_product=True,
        )


        self.variant_with_stock_tracking = ProductVariantFactory(
            product=ProductFactory(
                product_type=self.product_type,
                status=PublishableStatus.PUBLISHED,
            ),
            track_inventory=True,
            currency=settings.BASE_CURRENCY,
            price=normalize_amount_currencywise(100.00, settings.BASE_CURRENCY),
            cost_per_unit=50.00,
        )

    
        self.variant_without_stock_tracking = ProductVariantFactory(
            product=ProductFactory(
                product_type=self.product_type,
                status=PublishableStatus.PUBLISHED,
            ),
            track_inventory=True,
            currency=settings.BASE_CURRENCY,
            price=normalize_amount_currencywise(50.00, settings.BASE_CURRENCY),
            cost_per_unit=30.00,
        )

        self.variant_with_stock_trackin_backorder_allowed = ProductVariantFactory(
            product=ProductFactory(
                product_type=self.product_type,
                status=PublishableStatus.PUBLISHED,
            ),
            track_inventory=True,
            currency=settings.BASE_CURRENCY,
            price=normalize_amount_currencywise(50.00, settings.BASE_CURRENCY),
            cost_per_unit=30.00,
        )

        self.warehosue_us_central= WarehouseFactory()
        self.warehosue_us_east= WarehouseFactory()
        self.warehosue_us_west= WarehouseFactory()





        self.order_api_url = reverse('admin_order_create')
        self.order_estimate_api_url = reverse('admin_order_estimate')

    def test_order_stock_reservation_and_warehouse_update(self):
        """
        Test case to validate stock reservation and warehouse management during order creation.
        """
        currency = settings.BASE_CURRENCY

        
        order_payload_with_stock_tracking = {
            "variants": [
                {
                    "alias": self.variant_with_stock_tracking.alias,
                    "quantity": 10,
                },
            ]
        }

        order_payload_with_stock_tracking_backorder_allowed = {
            "variants": [
                {
                    "alias": self.variant_with_stock_trackin_backorder_allowed.alias,
                    "quantity": 10,
                },
            ]
        }

        order_payload_without_stock_tracking = {
            "variants": [
                {
                    "alias": self.variant_without_stock_tracking.alias,
                    "quantity": 10,
                },
            ]
        }

        order_response_with_stock_tracking = self.client.post(self.order_api_url, order_payload_with_stock_tracking)
        order_response_with_stock_tracking_backorder_allowed = self.client.post(self.order_api_url, order_payload_with_stock_tracking_backorder_allowed)
        order_response_without_stock_tracking = self.client.post(self.order_api_url, order_payload_without_stock_tracking)

        print(order_response_with_stock_tracking)

        # self.assertEqual(order_response_with_stock_tracking.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(order_response_with_stock_tracking_backorder_allowed.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(order_response_without_stock_tracking.status_code, status.HTTP_201_CREATED)