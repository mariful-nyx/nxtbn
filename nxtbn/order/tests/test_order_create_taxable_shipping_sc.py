import random
from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse
from nxtbn.core import PublishableStatus
from nxtbn.core.utils import normalize_amount_currencywise
from nxtbn.home.base_tests import BaseTestCase
from nxtbn.product import WeightUnits
from nxtbn.product.models import Product
from rest_framework.test import APIClient
from nxtbn.product.tests import ProductFactory, ProductTypeFactory, ProductVariantFactory
from nxtbn.shipping.tests import ShippingMethodFactory, ShippingRateFactory
from nxtbn.tax.tests import TaxClassFactory


class OrderCreateShippingRateTest(BaseTestCase):
    """
    Test case for Order Create API with proper shipping rate calculations.
    """

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.client.login(email='test@example.com', password='testpass')

        self.country = 'US'
        self.state_one = 'TX'
        self.state_two = 'NY'

        # Tax class
        self.tax_class = TaxClassFactory()

        # Shipping method
        self.shipping_method = ShippingMethodFactory(name='DHL-DTH')

        # Shipping rates
        self.shipping_rate_one = ShippingRateFactory(
            shipping_method=self.shipping_method,
            country=self.country,
            region=self.state_one,
            rate=normalize_amount_currencywise(10, 'USD'),
            weight_min=0,
            weight_max=5,  # 5kg
            currency='USD'
        )
        self.shipping_rate_two = ShippingRateFactory(
            shipping_method=self.shipping_method,
            country=self.country,
            region=self.state_two,
            rate=normalize_amount_currencywise(15, 'USD'),
            weight_min=0,
            weight_max=5,  # 5kg
            currency='USD'
        )

        self.order_api_url = reverse('order-create')
        self.order_estimate_api_url = reverse('order-estimate')

    def test_order_shipping_rate_calculation(self):
        """
        Test case to ensure shipping rates are accurately calculated based on product weights and regions.
        """
        currency = settings.BASE_CURRENCY

        # Create product type and products
        product_type = ProductTypeFactory(
            name=f"{currency} Product Type physical",
            track_stock=False,
            taxable=True,
            physical_product=True,
            # weight_unit=WeightUnits.GRAM,
        )

        # Create products and variants
        product_one = ProductFactory(
            product_type=product_type,
            tax_class=self.tax_class,
            status=PublishableStatus.PUBLISHED,
        )
        variant_one = ProductVariantFactory(
            product=product_one,
            track_inventory=False,
            currency=currency,
            price=normalize_amount_currencywise(20.26, currency),
            cost_per_unit=50.00,
            weight_value=578,  # 578 grams
        )

        product_two = ProductFactory(
            product_type=product_type,
            tax_class=self.tax_class,
            status=PublishableStatus.PUBLISHED,
        )
        variant_two = ProductVariantFactory(
            product=product_two,
            track_inventory=False,
            currency=currency,
            price=normalize_amount_currencywise(20.26, currency),
            cost_per_unit=50.00,
            weight_value=578,  # 578 grams
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
                    "quantity": 40,
                }
            ]
        }

        # Expected values
        total_weight = 40 * 578 * 2 / 1000  # Convert grams to kilograms
        shipping_rate = self.shipping_rate_two.rate if total_weight <= 5 else self.shipping_rate_two.rate + (total_weight - 5) * self.shipping_rate_two.incremental_rate
        expected_subtotal = 20.26 * 80  # 80 items total
        expected_total = expected_subtotal + float(shipping_rate)

        # Estimate Test
        order_estimate_response = self.client.post(self.order_estimate_api_url, order_payload, format='json')
        self.assertEqual(order_estimate_response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(order_estimate_response.data['subtotal'], expected_subtotal, places=2)
        self.assertAlmostEqual(order_estimate_response.data['total'], expected_total, places=2)

        # Order Create Test
        order_response = self.client.post(self.order_api_url, order_payload, format='json')
        self.assertEqual(order_response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(order_response.data['subtotal'], expected_subtotal, places=2)
        self.assertAlmostEqual(order_response.data['total'], expected_total, places=2)
