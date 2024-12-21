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
from nxtbn.purchase.tests import PurchaseOrderFactory, PurchaseOrderItemFactory
from nxtbn.shipping.models import ShippingRate
from nxtbn.shipping.tests import ShippingMethodFactory, ShippingRateFactory
from nxtbn.tax.tests import TaxClassFactory, TaxRateFactory
from babel.numbers import get_currency_precision, format_currency


from django.test.utils import override_settings

from nxtbn.warehouse.tests import WarehouseFactory


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class PurchangeOrderReceivingTest(BaseTestCase):
   
    def setUp(self):
        super().setUp()
        self.adminLogin()

        self.supplier = SupplierFactory()
        self.warehouse = WarehouseFactory()
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

        self.purchange = PurchaseOrderFactory(
            supplier=self.supplier,
            destination=self.warehouse,
            created_by=self.user,
            status=PurchaseStatus.DRAFT
        )

        self.purchage_item_one = PurchaseOrderItemFactory(
            purchase_order=self.purchange,
            variant=self.product_variant_one,
            ordered_quantity=10,
            unit_cost=Decimal('100.00')
        )
        self.purchage_item_two = PurchaseOrderItemFactory(
            purchase_order=self.purchange,
            variant=self.product_variant_two,
            ordered_quantity=8,
            unit_cost=Decimal('100.00')
        )
        self.purchage_item_three = PurchaseOrderItemFactory(
            purchase_order=self.purchange,
            variant=self.product_variant_three,
            ordered_quantity=3,
            unit_cost=Decimal('100.00')
        )
        self.purchage_item_four = PurchaseOrderItemFactory(
            purchase_order=self.purchange,
            variant=self.product_variant_four,
            ordered_quantity=250,
            unit_cost=Decimal('100.00')
        )

       

    def test_purchange_receiving(self):
        url = reverse('inventory-receiving', kwargs={'pk': self.purchange.pk})
        data = {
            'items': [
                {
                    'id': self.purchage_item_one.pk,
                    'received_quantity': 10,
                    'rejected_quantity': 0
                },
                {
                    'id': self.purchage_item_two.pk,
                    'received_quantity': 8,
                    'rejected_quantity': 0
                },
                {
                    'id': self.purchage_item_three.pk,
                    'received_quantity': 3,
                    'rejected_quantity': 0
                },
                {
                    'id': self.purchage_item_four.pk,
                    'received_quantity': 250,
                    'rejected_quantity': 0
                }
            ]
        }
        response = self.auth_client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        