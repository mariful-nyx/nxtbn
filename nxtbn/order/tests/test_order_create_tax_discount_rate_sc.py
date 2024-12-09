from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from nxtbn.core import PublishableStatus
from nxtbn.product.tests import ProductFactory, CategoryFactory, ProductTypeFactory, ProductVariantFactory
from nxtbn.tax.tests import TaxClassFactory, TaxRateFactory
from nxtbn.discount.tests import PromoCodeFactory, PromoCodeCustomerFactory, PromoCodeProductFactory # Assuming promo codes are defined here

from nxtbn.home.base_tests import BaseTestCase
from nxtbn.core.utils import normalize_amount_currencywise
from nxtbn.users.tests import UserFactory

from uuid import uuid4

from faker import Faker
import random

from django.utils import timezone
from nxtbn.payment import PaymentStatus

from datetime import timedelta

fake = Faker()


class OrderCreateMultiplePromoCodesTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.auth_client = APIClient()
        self.adminLogin()

        # Common setup
        self.country = 'US'
        self.state = 'NY'

        # Tax classes
        self.tax_class_15 = TaxClassFactory()
        self.tax_class_5 = TaxClassFactory()

        self.order_api_url = reverse('admin_order_create')
        self.order_estimate_api_url = reverse('admin_order_estimate')

    def _create_order_with_promo(self, promo_code, currency, params):
        """
        Helper method to create orders with a specific promo code.
        """
        # Set up tax rates
        TaxRateFactory(tax_class=self.tax_class_15, is_active=True, rate=15, country=self.country, state=self.state)
        TaxRateFactory(tax_class=self.tax_class_5, is_active=True, rate=5, country=self.country, state=self.state)

        # Create products and variants with 6 properties
        
        # Create products
        product_1 = ProductFactory(
            product_type=ProductTypeFactory(
                name=f"{currency} Product Type non-trackable, taxable 15% - {promo_code}",
                track_stock=False,
                taxable=True,
            ),
            tax_class=self.tax_class_15,
            status=PublishableStatus.PUBLISHED,
            category=CategoryFactory(
                name="cate1",
                description = "cate 1 description"
            )
        )

        product_2 = ProductFactory(
            product_type=ProductTypeFactory(
                name=f"{currency} Product Type non-trackable, non-taxable - {promo_code}",
                track_stock=False,
                taxable=False,
            ),
            tax_class=None,
            status=PublishableStatus.PUBLISHED,
            category=CategoryFactory(
                name="cate2",
                description = "cate 2 description"
            )
        )

        product_3 = ProductFactory(
            product_type=ProductTypeFactory(
                name=f"{currency} Product Type non-trackable, taxable 5% - {promo_code}",
                track_stock=False,
                taxable=True,
            ),
            tax_class=self.tax_class_5,
            status=PublishableStatus.PUBLISHED,
            category=CategoryFactory(
                name="cate3",
                description = "cate 3 description"
            )
        )

        product_4 = ProductFactory(
            product_type=ProductTypeFactory(
                name=f"{currency} Product Type 000 1 - {promo_code}",
                track_stock=True,
                taxable=False,
            ),
            tax_class=None,
            status=PublishableStatus.PUBLISHED,
            category=CategoryFactory(
                name="cate4",
                description = "cate 4 description"
            )
        )

        product_5 = ProductFactory(
            product_type=ProductTypeFactory(
                name=f"{currency} Product Type 2 - {promo_code}",
                track_stock=False,
                taxable=True,
            ),
            tax_class=self.tax_class_5,
            status=PublishableStatus.PUBLISHED,
            category=CategoryFactory(
                name="cate5",
                description = "cate 5 description"
            )
        )

        product_6 = ProductFactory(
            product_type=ProductTypeFactory(
                name=f"{currency} Product Type 4 - {promo_code}",
                track_stock=False,
                taxable=True,
            ),
            tax_class=self.tax_class_15,
            status=PublishableStatus.PUBLISHED,
            category=CategoryFactory(
                name="cate6",
                description = "cate 6 description"
            )
            
        )

        
  

        variant_payload = {}

        if params.get("applicable_variant") and params.get("applicable_product"):
            applicable_product = params.get("applicable_product")

            applicable_variant = ProductVariantFactory(
                product=applicable_product, 
                track_inventory=False,
                currency=currency,
                price=normalize_amount_currencywise(params['applicable_variant']['price'], currency),
                stock=params['applicable_variant']['stock'],
                cost_per_unit=params['applicable_variant']['cost_per_unit']
            )

            variant_payload = {
                "variants": [
                    {"alias": applicable_variant.alias, "quantity": 2}
                ]
            }
        else:
            variant_1 = ProductVariantFactory(
                product=product_1, 
                track_inventory=False,
                currency=currency,
                price=normalize_amount_currencywise(params['variant_1']['price'], currency),
                stock=params['variant_1']['stock'],
                cost_per_unit=params['variant_1']['cost_per_unit']
            )
            variant_2 = ProductVariantFactory(
                product=product_2, 
                track_inventory=False,
                currency=currency,
                price=normalize_amount_currencywise(params['variant_2']['price'], currency),
                stock=params['variant_2']['stock'],
                cost_per_unit=params['variant_2']['cost_per_unit']
            )
            variant_3 = ProductVariantFactory(
                product=product_3, 
                track_inventory=False,
                currency=currency,
                price=normalize_amount_currencywise(params['variant_3']['price'], currency),
                stock=params['variant_3']['stock'],
                cost_per_unit=params['variant_3']['cost_per_unit']
            )
            variant_4 = ProductVariantFactory(
                product=product_4, 
                track_inventory=False,
                currency=currency,
                price=normalize_amount_currencywise(params['variant_4']['price'], currency),
                stock=params['variant_4']['stock'],
                cost_per_unit=params['variant_4']['cost_per_unit']
            )
            variant_5 = ProductVariantFactory(
                product=product_5, 
                track_inventory=False,
                currency=currency,
                price=normalize_amount_currencywise(params['variant_5']['price'], currency),
                stock=params['variant_5']['stock'],
                cost_per_unit=params['variant_5']['cost_per_unit']
            )
            variant_6 = ProductVariantFactory(
                product=product_6, 
                track_inventory=False,
                currency=currency,
                price=normalize_amount_currencywise(params['variant_6']['price'], currency),
                stock=params['variant_6']['stock'],
                cost_per_unit=params['variant_6']['cost_per_unit']
            )
            variant_payload = {
                "variants": [
                    {"alias": variant_1.alias, "quantity": 2},
                    {"alias": variant_2.alias, "quantity": 3},
                    {"alias": variant_3.alias, "quantity": 4},
                    {"alias": variant_4.alias, "quantity": 5},
                    {"alias": variant_5.alias, "quantity": 6},
                    {"alias": variant_6.alias, "quantity": 7}
                ]
            }
        

        promocode_payload = {}

        if type(promo_code) == dict:
            promocode_payload = {
                'custom_discount_amount': promo_code
            }
        else:
            promocode_payload = {
                'promocode': promo_code
            }

        customer_payload = {}

        if params.get("customer_id"):
            customer_payload = {
                "customer_id" : params.get("customer_id")
            }
        else:
            customer_payload = {}

        # specific_customer = 
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
            **customer_payload,
            **promocode_payload,  # Applying promo code
            **variant_payload
        }


        # Estimate Test
        order_estimate_response = self.auth_client.post(self.order_estimate_api_url, 
                                                        order_payload, format='json', 
                                                        headers={'Accept-Currency': settings.BASE_CURRENCY}
                                                        )


        self.assertEqual(order_estimate_response.status_code, status.HTTP_200_OK)
        self.assertEqual(order_estimate_response.data['subtotal'], params['subtotal'])
        self.assertEqual(order_estimate_response.data['total'], params['total'])
        self.assertEqual(order_estimate_response.data['estimated_tax'], params['tax'])

        # Order Create Test
        order_response = self.auth_client.post(self.order_api_url, 
                                               order_payload, format='json',
                                               headers={'Accept-Currency': settings.BASE_CURRENCY}
                                               )
        self.assertEqual(order_response.status_code, status.HTTP_200_OK)
        self.assertEqual(order_response.data['subtotal'], params['subtotal'])
        self.assertEqual(order_response.data['total'], params['total'])
        self.assertEqual(order_response.data['estimated_tax'], params['tax'])




    def test_order_discount_and_tax_calculation_with_promo_20all(self):
        """
        Test Order creation with various promo codes and products having 6 properties.
        We will test 6 different promo codes for the order with 6 different products.
        """

        user = UserFactory(
            username = "test_user_1"
        )
        # Promo Codes
        promo_20all = PromoCodeFactory(code="20ALL", 
                                        code_type="PERCENTAGE", 
                                        value=20,   
                                        is_active=True,
                                        min_purchase_amount=0,
                                        min_purchase_period=None,
                                        redemption_limit=None,
                                        new_customers_only=False,)  # 20% discount
        


        if settings.BASE_CURRENCY == 'USD':
            self._create_order_with_promo(
                promo_code= promo_20all.code,
                currency="USD",
                params={
                    "subtotal": "$78.00",
                    "total": "$65.62",
                    "tax": "$3.22",
                    "customer_id": user.id,
                    "variant_1": {"price": 2.00, "cost_per_unit": 2.00, "stock": 10}, #*2
                    "variant_2": {"price": 3.00, "cost_per_unit": 4.00, "stock": 10}, #*3
                    "variant_3": {"price": 2.50, "cost_per_unit": 3.00, "stock": 10}, #*4
                    "variant_4": {"price": 3.50, "cost_per_unit": 2.00, "stock": 10}, #*5
                    "variant_5": {"price": 4.50, "cost_per_unit": 1.00, "stock": 10}, #*6
                    "variant_6": {"price": 1.50, "cost_per_unit": 1.00, "stock": 10} #*7
                }
            )

        if settings.BASE_CURRENCY == 'JPY':
            self._create_order_with_promo(
                promo_code= promo_20all.code,
                currency="JPY",
                params={
                    "subtotal": "¥131,600",
                    "total": "¥111,942",  
                    "tax": "¥6,662",
                    "customer_id": user.id,
                    "variant_1": {"price": 5000, "cost_per_unit": 4000, "stock": 10},
                    "variant_2": {"price": 3000, "cost_per_unit": 2500, "stock": 10}, 
                    "variant_3": {"price": 4550, "cost_per_unit": 3500, "stock": 10}, 
                    "variant_4": {"price": 6550, "cost_per_unit": 3500, "stock": 10}, 
                    "variant_5": {"price": 5550, "cost_per_unit": 3500, "stock": 10}, 
                    "variant_6": {"price": 4050, "cost_per_unit": 3500, "stock": 10}, 
                }
            )

        if settings.BASE_CURRENCY == 'KWD':
            self._create_order_with_promo(
                promo_code= promo_20all.code,
                currency="KWD",
                params={
                    "subtotal": "KWD78.000",
                    "total": "KWD65.620",  
                    "tax": "KWD3.220",
                    "customer_id": user.id,
                    "variant_1": {"price": 2.00, "cost_per_unit": 2.00, "stock": 10}, 
                    "variant_2": {"price": 3.00, "cost_per_unit": 4.00, "stock": 10},
                    "variant_3": {"price": 2.50, "cost_per_unit": 3.00, "stock": 10},
                    "variant_4": {"price": 3.50, "cost_per_unit": 2.00, "stock": 10}, 
                    "variant_5": {"price": 4.50, "cost_per_unit": 1.00, "stock": 10}, 
                    "variant_6": {"price": 1.50, "cost_per_unit": 1.00, "stock": 10}, 
                }
            )



    def test_order_discount_and_tax_calculation_with_promo_flat200(self):
        user = UserFactory(
            username = "test_user_2"
        )
        if settings.BASE_CURRENCY == 'USD':
            self._create_order_with_promo(
                promo_code= {"name": "200USD", "price": "200"},
                currency="USD",
                params={
                    "subtotal": "$348.00",
                    "total": "$157.58",
                    "tax": "$9.58",
                    "customer_id": user.id,
                    "variant_1": {"price": 12.00, "cost_per_unit": 2.00, "stock": 10}, 
                    "variant_2": {"price": 13.00, "cost_per_unit": 4.00, "stock": 10},
                    "variant_3": {"price": 12.50, "cost_per_unit": 3.00, "stock": 10},
                    "variant_4": {"price": 13.50, "cost_per_unit": 2.00, "stock": 10}, 
                    "variant_5": {"price": 14.50, "cost_per_unit": 1.00, "stock": 10}, 
                    "variant_6": {"price": 11.50, "cost_per_unit": 1.00, "stock": 10}
                }
            )

        if settings.BASE_CURRENCY == 'JPY':
            self._create_order_with_promo(
                promo_code= {"name": "300JPY", "price": "300"},
                currency="JPY",
                params={
                    "subtotal": "¥131,600",
                    "total": "¥139,609",  
                    "tax": "¥8,309",
                    "customer_id": user.id,
                    "variant_1": {"price": 5000, "cost_per_unit": 4000, "stock": 10},
                    "variant_2": {"price": 3000, "cost_per_unit": 2500, "stock": 10}, 
                    "variant_3": {"price": 4550, "cost_per_unit": 3500, "stock": 10}, 
                    "variant_4": {"price": 6550, "cost_per_unit": 3500, "stock": 10}, 
                    "variant_5": {"price": 5550, "cost_per_unit": 3500, "stock": 10}, 
                    "variant_6": {"price": 4050, "cost_per_unit": 3500, "stock": 10}, 
                }
            )

        if settings.BASE_CURRENCY == 'KWD':
            self._create_order_with_promo(
                promo_code= {"name": "200KYD", "price": "200"},
                currency="KWD",
                params={
                    "subtotal": "KWD348.000",
                    "total": "KWD157.580",  
                    "tax": "KWD9.580",
                    "customer_id": user.id,
                    "variant_1": {"price": 12.00, "cost_per_unit": 2.00, "stock": 10}, 
                    "variant_2": {"price": 13.00, "cost_per_unit": 4.00, "stock": 10},
                    "variant_3": {"price": 12.50, "cost_per_unit": 3.00, "stock": 10},
                    "variant_4": {"price": 13.50, "cost_per_unit": 2.00, "stock": 10}, 
                    "variant_5": {"price": 14.50, "cost_per_unit": 1.00, "stock": 10}, 
                    "variant_6": {"price": 11.50, "cost_per_unit": 1.00, "stock": 10}, 
                }
            )


    def test_order_discount_and_tax_calculation_with_promo_gold5(self):
        user = UserFactory(
            username = f"test_user_3 "
        )
        promo_gold5 = PromoCodeFactory(code="GOLDCUSTOMER5", code_type="PERCENTAGE", value=5, is_active=True, min_purchase_amount=None, min_purchase_period=None, new_customers_only=False)  # 5% for Gold customers
        
        apply_customer = PromoCodeCustomerFactory(
            promo_code = promo_gold5,
            customer = user
        )
        
        if apply_customer and promo_gold5:
            if settings.BASE_CURRENCY == 'USD':
                self._create_order_with_promo(
                    promo_code= promo_gold5.code,
                    currency="USD",
                    params={
                        "subtotal": "$78.00",
                        "total": "$77.92",
                        "tax": "$3.82",
                        "customer_id": user.id,
                        "variant_1": {"price": 2.00, "cost_per_unit": 2.00, "stock": 10}, 
                        "variant_2": {"price": 3.00, "cost_per_unit": 4.00, "stock": 10},
                        "variant_3": {"price": 2.50, "cost_per_unit": 3.00, "stock": 10},
                        "variant_4": {"price": 3.50, "cost_per_unit": 2.00, "stock": 10}, 
                        "variant_5": {"price": 4.50, "cost_per_unit": 1.00, "stock": 10}, 
                        "variant_6": {"price": 1.50, "cost_per_unit": 1.00, "stock": 10}
                    }
                )

            if settings.BASE_CURRENCY == 'JPY':
                self._create_order_with_promo(
                    promo_code= promo_gold5.code,
                    currency="JPY",
                    params={
                        "subtotal": "¥131,600",
                        "total": "¥132,931",  
                        "tax": "¥7,911",
                        "customer_id": user.id,
                        "variant_1": {"price": 5000, "cost_per_unit": 4000, "stock": 10},
                        "variant_2": {"price": 3000, "cost_per_unit": 2500, "stock": 10}, 
                        "variant_3": {"price": 4550, "cost_per_unit": 3500, "stock": 10}, 
                        "variant_4": {"price": 6550, "cost_per_unit": 3500, "stock": 10}, 
                        "variant_5": {"price": 5550, "cost_per_unit": 3500, "stock": 10}, 
                        "variant_6": {"price": 4050, "cost_per_unit": 3500, "stock": 10}, 
                    }
                )

            if settings.BASE_CURRENCY == 'KWD':
                self._create_order_with_promo(
                    promo_code= promo_gold5.code,
                    currency="KWD",
                    params={
                        "subtotal": "KWD78.000",
                        "total": "KWD77.924",  
                        "tax": "KWD3.824",
                        "customer_id": user.id,
                        "variant_1": {"price": 2.00, "cost_per_unit": 2.00, "stock": 10}, 
                        "variant_2": {"price": 3.00, "cost_per_unit": 4.00, "stock": 10},
                        "variant_3": {"price": 2.50, "cost_per_unit": 3.00, "stock": 10},
                        "variant_4": {"price": 3.50, "cost_per_unit": 2.00, "stock": 10}, 
                        "variant_5": {"price": 4.50, "cost_per_unit": 1.00, "stock": 10}, 
                        "variant_6": {"price": 1.50, "cost_per_unit": 1.00, "stock": 10}, 
                    }
                )

        
    def test_order_discount_and_tax_calculation_with_promo_sell5(self):

        user = UserFactory(
            username="test_user_4"
        )


        product = ProductFactory(
            product_type=ProductTypeFactory(
                name=f"Product Type non-trackable, taxable 15% ",
                track_stock=False,
                taxable=True,
            ),
            tax_class=self.tax_class_15,
            status=PublishableStatus.PUBLISHED,
        )

        variant = ProductVariantFactory(
                product=product, 
                track_inventory=False,
                currency= settings.BASE_CURRENCY,
                price=normalize_amount_currencywise(10000, settings.BASE_CURRENCY),
                stock=20,
                cost_per_unit=3
            )

       
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
            "customer_id": user.id,
            "promocode": "",
            "variants" : [
                {"alias": variant.alias, "quantity": 2},
            ]
        }

        min_purchased = self.auth_client.post(self.order_api_url, 
                                order_payload, format='json',
                                headers={'Accept-Currency': settings.BASE_CURRENCY}
                            )

        if min_purchased:
            promo_sell5 = PromoCodeFactory(code="SELL5", 
                                            code_type="PERCENTAGE", 
                                            value=5,  
                                            is_active=True,
                                            min_purchase_amount=40,
                                            # min_purchase_period=timedelta(days=10), 
                                            redemption_limit=None,
                                            new_customers_only=False)


            ProductFactory(
                product_type=ProductTypeFactory(
                    name = f"{settings.BASE_CURRENCY} product type",
                    track_stock = True,
                    taxable = True
                ),
                status = PublishableStatus.PUBLISHED,
                category=CategoryFactory(
                    name="cat-min-purchase",
                    description = "cate-min-purchase description"
                )
            )

            apply_customer = PromoCodeCustomerFactory(
                promo_code = promo_sell5,
                customer = user
            )

            if apply_customer:
            
                if settings.BASE_CURRENCY == 'USD':
                    self._create_order_with_promo(
                        promo_code= promo_sell5.code,
                        currency="USD",
                        params={
                            "subtotal": "$1,316.00",
                            "total": "$1,329.31",
                            "tax": "$79.11",
                            "customer_id": user.id,
                            "variant_1": {"price": 50.00, "cost_per_unit": 40.00, "stock": 10},
                            "variant_2": {"price": 30.00, "cost_per_unit": 25.00, "stock": 10}, 
                            "variant_3": {"price": 45.50, "cost_per_unit": 35.00, "stock": 10}, 
                            "variant_4": {"price": 65.50, "cost_per_unit": 35.00, "stock": 10}, 
                            "variant_5": {"price": 55.50, "cost_per_unit": 35.00, "stock": 10}, 
                            "variant_6": {"price": 40.50, "cost_per_unit": 35.00, "stock": 10}, 
                        }
                    )

                if settings.BASE_CURRENCY == 'JPY':
                    self._create_order_with_promo(
                        promo_code= promo_sell5.code,
                        currency="JPY",
                        params={
                            "subtotal": "¥131,600",
                            "total": "¥132,931",  
                            "tax": "¥7,911",
                            "customer_id": user.id,
                            "variant_1": {"price": 5000, "cost_per_unit": 4000, "stock": 10},
                            "variant_2": {"price": 3000, "cost_per_unit": 2500, "stock": 10}, 
                            "variant_3": {"price": 4550, "cost_per_unit": 3500, "stock": 10}, 
                            "variant_4": {"price": 6550, "cost_per_unit": 3500, "stock": 10}, 
                            "variant_5": {"price": 5550, "cost_per_unit": 3500, "stock": 10}, 
                            "variant_6": {"price": 4050, "cost_per_unit": 3500, "stock": 10}, 
                        }
                    )

                if settings.BASE_CURRENCY == 'KWD':
                    self._create_order_with_promo(
                        promo_code= promo_sell5.code,
                        currency="KWD",
                        params={
                            "subtotal": "KWD78.000",
                            "total": "KWD77.924",  
                            "tax": "KWD3.824",
                            "customer_id": user.id,
                            "variant_1": {"price": 2.00, "cost_per_unit": 2.00, "stock": 10}, 
                            "variant_2": {"price": 3.00, "cost_per_unit": 4.00, "stock": 10},
                            "variant_3": {"price": 2.50, "cost_per_unit": 3.00, "stock": 10},
                            "variant_4": {"price": 3.50, "cost_per_unit": 2.00, "stock": 10}, 
                            "variant_5": {"price": 4.50, "cost_per_unit": 1.00, "stock": 10}, 
                            "variant_6": {"price": 1.50, "cost_per_unit": 1.00, "stock": 10}, 
                        }
                    )



        
    def test_order_discount_and_tax_calculation_with_promo_clearance20(self):
        product = ProductFactory(
            product_type = ProductTypeFactory(
                taxable = True,
                track_stock = True
            ),
            tax_class=self.tax_class_15,
            status=PublishableStatus.PUBLISHED,
        )

        promo_clearance20 = PromoCodeFactory(code="CLEARANCE20", 
                                             code_type="PERCENTAGE", 
                                             value=20, 
                                            is_active=True,
                                            min_purchase_amount=0,
                                            min_purchase_period=None,
                                            redemption_limit=None,
                                            new_customers_only=False,)


        apply_product = PromoCodeProductFactory(
            promo_code=promo_clearance20,
            product=product
        )

        user = UserFactory(
            username="test_user_5"
        )

        

        if promo_clearance20 and apply_product and user:

            if settings.BASE_CURRENCY == 'USD':
                self._create_order_with_promo(
                    promo_code= promo_clearance20.code,
                    currency="USD",
                    params={
                        "subtotal": "$7.00",
                        "total": "$6.44",
                        "tax": "$0.84",
                        "customer_id": user.id,
                        "applicable_variant": {"price": 3.50, "cost_per_unit": 1.00, "stock": 10},
                        "applicable_product" : product
                    }
                )

            if settings.BASE_CURRENCY == 'JPY':
                self._create_order_with_promo(
                    promo_code= promo_clearance20.code,
                    currency="JPY",
                    params={
                        "subtotal": "¥7,000",
                        "total": "¥6,440",  
                        "tax": "¥840",
                        "customer_id": user.id,
                        "applicable_variant": {"price": 3500, "cost_per_unit": 1.00, "stock": 10},
                        "applicable_product" : product
                    }
                )

            if settings.BASE_CURRENCY == 'KWD':
                self._create_order_with_promo(
                    promo_code= promo_clearance20.code,
                    currency="KWD",
                    params={
                        "subtotal": "KWD7.000",
                        "total": "KWD6.440",  
                        "tax": "KWD0.840",
                        "customer_id": user.id,
                        "applicable_variant": {"price": 3.50, "cost_per_unit": 1.00, "stock": 10},
                        "applicable_product" : product 
                    }
                )