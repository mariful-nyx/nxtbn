import random
from decimal import Decimal
from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse
from nxtbn.core import PublishableStatus
from nxtbn.core.utils import build_currency_amount, normalize_amount_currencywise
from nxtbn.home.base_tests import BaseTestCase
from nxtbn.order.proccesor.views import get_shipping_rate_instance
from nxtbn.product import WeightUnits
from nxtbn.product.models import Product
from rest_framework.test import APIClient
from nxtbn.product.tests import ProductFactory, ProductTypeFactory, ProductVariantFactory, SupplierFactory
from nxtbn.purchase import PurchaseStatus
from nxtbn.purchase.models import PurchaseOrderItem
from nxtbn.purchase.tests import PurchaseOrderFactory, PurchaseOrderItemFactory
from nxtbn.shipping.models import ShippingRate
from nxtbn.shipping.tests import ShippingMethodFactory, ShippingRateFactory
from nxtbn.tax.tests import TaxClassFactory, TaxRateFactory
from babel.numbers import get_currency_precision, format_currency
import datetime
from django.test.utils import override_settings
from nxtbn.warehouse.models import Stock, StockTransferItem
from nxtbn.warehouse.tests import StockFactory, WarehouseFactory
from datetime import date


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class StockTransferCreateUpdateAPITest(BaseTestCase):
   
    def setUp(self):
        super().setUp()
        self.adminLogin()

        self.supplier = SupplierFactory()
        self.from_warehouse = WarehouseFactory()
        self.to_warehouse = WarehouseFactory()
        self.product = ProductFactory()

        self.product_variant_one = ProductVariantFactory(
            product=self.product,
            price=Decimal('100.00'),
            cost_per_unit=Decimal('100.00')
        )
        self.product_variant_two = ProductVariantFactory(
            product=self.product,
            price=Decimal('100.00'),
            cost_per_unit=Decimal('100.00')
        )
        self.product_variant_three = ProductVariantFactory(
            product=self.product,
            price=Decimal('100.00'),
            cost_per_unit=Decimal('100.00')
        )
        self.product_variant_four = ProductVariantFactory(
            product=self.product,
            price=Decimal('100.00'),
            cost_per_unit=Decimal('100.00')
        )

        self.product_variant_five = ProductVariantFactory(
            product=self.product,
            price=Decimal('100.00'),
            cost_per_unit=Decimal('100.00')
        )

        self.stock_from_warehouse_varinat_one = StockFactory(
            warehouse=self.from_warehouse,
            product_variant=self.product_variant_one,
            quantity=10
        )

        self.stock_from_warehouse_varinat_two = StockFactory(
            warehouse=self.from_warehouse,
            product_variant=self.product_variant_two,
            quantity=100
        )

        self.stock_from_warehouse_varinat_three = StockFactory(
            warehouse=self.from_warehouse,
            product_variant=self.product_variant_three,
            quantity=5
        )

        self.stock_to_warehouse_varinat_four = StockFactory(
            warehouse=self.from_warehouse,
            product_variant=self.product_variant_four,
            quantity=10
        )

       

    def test_stock_transfer_create_update(self):
        stock_transfer_create_url = reverse('stock-transfer-list')

        payload = {
            "from_warehouse": self.from_warehouse.id,
            "to_warehouse": self.to_warehouse.id,
            "items": [
                {
                    "quantity": 3,
                    "variant": self.product_variant_one.id
                },
                {
                    "quantity": 5,
                    "variant": self.product_variant_two.id
                },
                {
                    "quantity": 15, # more quantity than available in stock
                    "variant": self.product_variant_three.id
                },
            ]
        }
        response_stock_transfer_create = self.auth_client.post(stock_transfer_create_url, payload, format='json')
        self.assertEqual(response_stock_transfer_create.status_code, status.HTTP_400_BAD_REQUEST) # raise error as insufficient stock

        payload_stock_missing = {
            "from_warehouse": self.from_warehouse.id,
            "to_warehouse": self.to_warehouse.id,
            "items": [
                {
                    "quantity": 3,
                    "variant": self.product_variant_five.id # stock is missing in source warehouse
                },
            ]
        }

        response_stock_transfer_create_stock_missing = self.auth_client.post(stock_transfer_create_url, payload_stock_missing, format='json')
        self.assertEqual(response_stock_transfer_create_stock_missing.status_code, status.HTTP_400_BAD_REQUEST)

        payload_success = {
            "from_warehouse": self.from_warehouse.id,
            "to_warehouse": self.to_warehouse.id,
            "items": [
                {
                    "quantity": 3,
                    "variant": self.product_variant_one.id
                },
                {
                    "quantity": 3,
                    "variant": self.product_variant_two.id
                },
                {
                    "quantity": 3,
                    "variant": self.product_variant_three.id
                },
            ]
        }

        response_stock_transfer_create = self.auth_client.post(stock_transfer_create_url, payload_success, format='json')
        self.assertEqual(response_stock_transfer_create.status_code, status.HTTP_201_CREATED)


        stock_transfer_id = response_stock_transfer_create.json()['id']
        stock_transfer_detail_url = reverse('stock-transfer-detail', kwargs={'id': stock_transfer_id})

        updated_payload = { # in edit adding new item and another item deleted and quantity updated
            "from_warehouse": self.from_warehouse.id,
            "to_warehouse": self.to_warehouse.id,
            "items": [
                {
                    "quantity": 3,
                    "variant": self.product_variant_one.id
                },
                {
                    "quantity": 3,
                    "variant": self.product_variant_two.id
                },
                {
                    "quantity": 3,
                    "variant": self.product_variant_four.id
                },
            ]
        }
        response_stock_transfer_update = self.auth_client.put(stock_transfer_detail_url, updated_payload, format='json')
        self.assertEqual(response_stock_transfer_update.status_code, status.HTTP_200_OK)
        
        stock_transfer_detail_response = self.auth_client.get(stock_transfer_detail_url, format='json')
        self.assertEqual(len(stock_transfer_detail_response.json()["items"]), 3)

        self.assertEqual(stock_transfer_detail_response.json()["items"][0]["quantity"], 3)
        self.assertEqual(stock_transfer_detail_response.json()["items"][1]["quantity"], 3)
        self.assertEqual(stock_transfer_detail_response.json()["items"][2]["quantity"], 3)

       
        with self.assertRaises(StockTransferItem.DoesNotExist):
            StockTransferItem.objects.get(stock_transfer_id=stock_transfer_id, variant=self.product_variant_three.id)



        # ==================================
        # Test for stock transfer receive
        # ==================================

        # at first stock transfer mark as in transit
        # stock_transfer_mark_as_transit_url = reverse('stock-transfer-mark-as-in-transit', kwargs={'pk': stock_transfer_id})

        # response_stock_transfer_mark_as_transit = self.auth_client.put(stock_transfer_mark_as_transit_url, format='json')
        # self.assertEqual(response_stock_transfer_mark_as_transit.status_code, status.HTTP_200_OK)
        # print(response_stock_transfer_mark_as_transit.data)


    def test_puchase_create_with_blank_items(self):
        purchase_create_url = reverse('stock-transfer-list')

        payload = {
            "from_warehouse": self.from_warehouse.id,
            "to_warehouse": self.to_warehouse.id,
            "items": []
        }
        response_purchase_create = self.auth_client.post(purchase_create_url, payload, format='json')
        self.assertEqual(response_purchase_create.status_code, status.HTTP_400_BAD_REQUEST)

