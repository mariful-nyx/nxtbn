import random
from decimal import Decimal
from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse
from nxtbn.core import PublishableStatus
from nxtbn.core.utils import build_currency_amount, normalize_amount_currencywise
from nxtbn.home.base_tests import BaseTestCase
from nxtbn.product import WeightUnits
from nxtbn.product.models import Product
from rest_framework.test import APIClient
from nxtbn.product.tests import ProductFactory, ProductTypeFactory, ProductVariantFactory
from nxtbn.shipping.models import ShippingRate
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
        self.state = 'NY'

        # Tax class
        self.tax_class = TaxClassFactory()

        # Shipping method
        self.shipping_method = ShippingMethodFactory(name='DHL-DTH')

        # Shipping rates
        self.input_weight_min = 0
        self.input_weight_max = 5 # 5kg
        self.input_rate = 15 #15 USD
        self.input_incremental_rate = 3 #3 USD
       
        ShippingRateFactory(
            shipping_method=self.shipping_method,
            country=self.country,
            region=self.state,
            rate=normalize_amount_currencywise(self.input_rate, settings.BASE_CURRENCY),
            weight_min=self.input_weight_min,
            weight_max=self.input_weight_max,  
            currency=settings.BASE_CURRENCY,
            incremental_rate=normalize_amount_currencywise(self.input_incremental_rate, settings.BASE_CURRENCY)
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
        total_weight = Decimal(40 * 578 * 2 / 1000)  # Convert grams to kilograms and cast to Decimal: expected 46.24 kg

        shipping_rate_instance = ShippingRate.objects.filter(
            region=self.state,
            weight_min__lte=total_weight,
            weight_max__gte=total_weight
        )

        if shipping_rate_instance.exists():
            self.shipping_rate = shipping_rate_instance.first().rate # expected 15
            self.incremental_rate = shipping_rate_instance.first().incremental_rate # expected 3
        else:
            self.shipping_rate = 0
            self.incremental_rate = 0


        shipping_rate = (
            self.shipping_rate
            if total_weight <= self.input_weight_max
            else self.shipping_rate + (total_weight - Decimal(5)) * self.incremental_rate
        ) # 15 + (46.24 - 5) * 3 = 15 + 41.24 * 3 = 15 + 123.72 = 138.72
        expected_subtotal = Decimal(20.26 * 80)  # 20.26 * 80 = 1620.8
        expected_total = expected_subtotal + shipping_rate # 1620.8 + 138.72 = 1759.52


        expected_total_fr = build_currency_amount(expected_total, currency, locale='en_US')
        expected_subtotal_fr = build_currency_amount(expected_subtotal, currency, locale='en_US')

        

        # Estimate Test
        order_estimate_response = self.client.post(self.order_estimate_api_url, order_payload, format='json')

        self.assertEqual(order_estimate_response.status_code, status.HTTP_200_OK)
        self.assertEqual(order_estimate_response.data['subtotal'], expected_subtotal_fr)
        self.assertEqual(order_estimate_response.data['total'], expected_total_fr)

        # Order Create Test
        order_response = self.client.post(self.order_api_url, order_payload, format='json')
        self.assertEqual(order_response.status_code, status.HTTP_200_OK)
        self.assertEqual(order_response.data['subtotal'], expected_subtotal_fr)
        self.assertEqual(order_response.data['total'], expected_total_fr)
