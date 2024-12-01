# test case for single currency mode
import random
import sys
from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse
from nxtbn.core import PublishableStatus
from nxtbn.core.utils import normalize_amount_currencywise
from nxtbn.home.base_tests import BaseTestCase
from nxtbn.product import WeightUnits
from nxtbn.product.models import Product, ProductType
from rest_framework.test import APIClient
from nxtbn.product.tests import ProductFactory, ProductTypeFactory, ProductVariantFactory
from nxtbn.shipping.tests import ShippingMethodFactory, ShippingRateFactory
from nxtbn.tax.tests import TaxClassFactory, TaxRateFactory


class OrderCreateShippingRate(BaseTestCase):
    """
    Test case for Order Create API with a single currency mode.
    Ensures accuracy in calculations shipping rates for different shipping methods and product weight and region.
    """

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.client.login(email='test@example.com', password='testpass')

        # Define common properties
        self.country = 'US'  # State specific, if state not matched, then NationWide
        self.state_two = 'NY'
        self.state_three = 'CA'

        self.country_two = 'SG'  # No State, NationWide

        # Tax class
        self.tax_class = TaxClassFactory()

        self.order_api_url = reverse('order-create')
        self.order_estimate_api_url = reverse('order-eastimate')

    def _test_order_for_currency(self, currency, params):
        """
        Helper method to test order create and estimate for a specific currency.
        Dynamically creates a variant based on provided params.
        """
        # Create product type and product
        product_type = ProductTypeFactory(
            name=f"{currency} Product Type physical",
            track_stock=False,
            taxable=True,
            physical_product=True,
            weight_unit=WeightUnits.GRAM,
        )
        product_one = ProductFactory(
            product_type=product_type,
            tax_class=self.tax_class,
            status=PublishableStatus.PUBLISHED,
        )

        # Create variant
        variant_one = ProductVariantFactory(
            product=product_one,
            track_inventory=False,
            currency=currency,
            price=normalize_amount_currencywise(params['price'], currency),
            cost_per_unit=params['cost_per_unit'],
        )

        product_two = ProductFactory(
            product_type=product_type,
            tax_class=self.tax_class,
            status=PublishableStatus.PUBLISHED,
        )

        # Create variant
        variant_two = ProductVariantFactory(
            product=product_two,
            track_inventory=False,
            currency=currency,
            price=normalize_amount_currencywise(params['price'], currency),
            cost_per_unit=params['cost_per_unit'],
        )

        # Create shipping methods
        shipping_method = ShippingMethodFactory(
            name='DHL-DTH'
        )

        # Create shipping rates
        shipping_rate_one = ShippingRateFactory(
            shipping_method=shipping_method,
            country=self.country,
            region=self.state_two,
            rate=normalize_amount_currencywise(10, currency),
            weight_min=0,
            weight_max=5,  # 5kg
            currency=currency
        )
        shipping_rate_one = ShippingRateFactory(
            shipping_method=shipping_method,
            country=self.country,
            region=self.state_two,
            rate=normalize_amount_currencywise(10, currency),
            weight_min=0,
            weight_max=5,  # 5kg
            currency=currency
        )

        # Payload for order
        order_payload = {
            "shipping_address": {
                "country": self.country,
                "state": self.state_two,
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
                "state": self.state_two,
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
                    "alias": variant_one.alias,
                    "quantity": 40,
                },
                {
                    "alias": variant_two.alias,
                    "quantity": 1,
                }
            ]
        }

        # Estimate Test
        order_estimate_response = self.client.post(self.order_estimate_api_url, order_payload, format='json', headers={'Accept-Currency': settings.BASE_CURRENCY})
        self.assertEqual(order_estimate_response.status_code, status.HTTP_200_OK)
        self.assertEqual(order_estimate_response.data['subtotal'], params['subtotal'])
        self.assertEqual(order_estimate_response.data['total'], params['total'])
        self.assertEqual(order_estimate_response.data['estimated_tax'], params['tax'])

        # Order Create Test
        order_response = self.client.post(self.order_api_url, order_payload, format='json', headers={'Accept-Currency': settings.BASE_CURRENCY})
        self.assertEqual(order_response.status_code, status.HTTP_200_OK)
        self.assertEqual(order_response.data['subtotal'], params['subtotal'])
        self.assertEqual(order_response.data['total'], params['total'])
        self.assertEqual(order_response.data['estimated_tax'], params['tax'])

    def test_order_for_all_currencies(self):
        """
        Test order creation and estimation for all currencies: USD, JPY, KWD.
        """
        # USD Test
        if settings.BASE_CURRENCY == 'USD':
            self._test_order_for_currency(
                "USD",
                {
                    # Expected output
                    "subtotal": "$60.78",
                    "total": "$69.90",
                    "tax": "$9.12",

                    # Variant creation parameters
                    "price": 20.26,
                    "cost_per_unit": 50.00,
                    "tax_rate": 15,  # 15%
                    "stock": 10,
                    "weight": 5,
                    "weight_unit": WeightUnits.GRAM,
                }
            )

        # JPY Test
        if settings.BASE_CURRENCY == 'JPY':
            self._test_order_for_currency(
                "JPY",
                {
                    # Expected output
                    "subtotal": "¥6,000",
                    "total": "¥6,900",
                    "tax": "¥900",

                    # Variant creation parameters
                    "price": 2000,
                    "cost_per_unit": 5000,
                    "tax_rate": 15,  # 15%
                    "stock": 10,
                    "weight": 5,
                    "weight_unit": WeightUnits.GRAM,
                }
            )

        # KWD Test
        if settings.BASE_CURRENCY == 'KWD':
            self._test_order_for_currency(
                "KWD",
                {
                    # Expected output
                    "subtotal": "KWD60.702",
                    "total": "KWD69.807",
                    "tax": "KWD9.105",

                    # Variant creation parameters
                    "price": 20.234,
                    "cost_per_unit": 15.500,
                    "tax_rate": 15,  # 15%
                    "stock": 10,
                    "weight": 5,
                    "weight_unit": WeightUnits.GRAM,
                }
            )
