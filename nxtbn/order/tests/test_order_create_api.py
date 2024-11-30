import random
import sys
from django.conf import settings
from rest_framework import status

from rest_framework.reverse import reverse

from nxtbn.core import PublishableStatus
from nxtbn.core.utils import normalize_amount_currencywise
from nxtbn.home.base_tests import BaseTestCase

from django.utils import timezone

from nxtbn.product.models import Product, ProductType
from rest_framework.test import APIClient

from nxtbn.product.tests import ProductFactory, ProductTypeFactory, ProductVariantFactory
from nxtbn.tax.tests import TaxClassFactory, TaxRateFactory




class OrderCreateNoTrackableTaxableAPI(BaseTestCase):
   

    """
        Test Case for Order Create API with a taxable product that has no stock tracking.
        This test case ensures that a product variant with no stock tracking and taxable status is created successfully.
        The product price is set to $20.26 USD with a tax rate of 15%, and the shipping address is in US, NY.
        The tax rate should be applied correctly for this location. Total items in the order are 3.
        Expected Output:
        - Subtotal: $60.78 (rounded to 2 decimal places)
        - Tax: $9.12 (rounded to 2 decimal places)
        - Total: $69.90 (rounded to 2 decimal places)
        The test will verify if the expected calculations are returned in the API response.
    """
    
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.client.login(email='test@example.com', password='testpass')

        self.country = 'US'
        self.state = 'NY'
        
        self.tax_class = TaxClassFactory()
        self.tax_rate = TaxRateFactory(
            tax_class=self.tax_class,
            is_active=True,
            rate = 15, # 15%
            country = self.country,
            state = self.state
        )
        self.product_type = ProductTypeFactory(
            name="Don't track stock but taxable",
            track_stock=False,
            taxable=True,
        )
        self.product = ProductFactory(
            product_type=self.product_type,
            tax_class=self.tax_class,
            status=PublishableStatus.PUBLISHED,
        )

        self.variants = ProductVariantFactory(
            product=self.product,
            track_inventory=False,
            currency='USD',
            price=normalize_amount_currencywise(20.26, settings.BASE_CURRENCY), # $20.26 USD
            stock=10,
            cost_per_unit=50,
        )

        self.order_api_url = reverse('order-create')
        self.order_eastimate_api_url = reverse('order-eastimate')



    def test_order_create_api(self):
        order_payload = {
            "shipping_address": {
                "country": self.country,
                "state": self.state,
                "street_address": "123 Main St",
                "city": "New York",
                "postal_code": "10001",
                "email": "test@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "1234567890"
            },
            "billing_address": {
                "country": self.country,
                "state": self.state,
                "street_address": "123 Main St",
                "city": "New York",
                "postal_code": "10001",
                "email": "test@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "1234567890"
            },
            "variants": [
                {
                    "alias": self.variants.alias,
                    "quantity": 3,
                }
            ]
        }

        # Eastimation Test
        order_eastimate_response = self.client.post(self.order_eastimate_api_url, order_payload, format='json')
        self.assertEqual(order_eastimate_response.status_code, status.HTTP_200_OK)
        self.assertEqual(order_eastimate_response.data['subtotal'], '$60.78')
        self.assertEqual(order_eastimate_response.data['total'], '$69.90')
        self.assertEqual(order_eastimate_response.data['estimated_tax'], '$9.12')
        self.assertEqual(order_eastimate_response.data['discount'], '$0.00')
        self.assertEqual(order_eastimate_response.data['total_items'], 3)
        self.assertEqual(order_eastimate_response.data['shipping_fee'], '$0.00')

        # Order Create Test
        order_response = self.client.post(self.order_api_url, order_payload, format='json')
        self.assertEqual(order_response.status_code, status.HTTP_200_OK)
        self.assertEqual(order_response.data['subtotal'], '$60.78')
        self.assertEqual(order_response.data['total'], '$69.90')
        self.assertEqual(order_response.data['estimated_tax'], '$9.12')
        self.assertEqual(order_response.data['discount'], '$0.00')
        self.assertEqual(order_response.data['total_items'], 3)
        self.assertEqual(order_response.data['shipping_fee'], '$0.00')