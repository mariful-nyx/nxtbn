import random
import sys
from rest_framework import status

from rest_framework.reverse import reverse

from nxtbn.core import PublishableStatus
from nxtbn.home.base_tests import BaseTestCase

from django.utils import timezone

from nxtbn.product.models import Product, ProductType
from rest_framework.test import APIClient




class ProductAndRelatedCreateAPITest(BaseTestCase):
    
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.url = reverse('signup')
        self.client.login(email='test@example.com', password='testpass')
        
        # Create ProductType
        self.product_type_data = {
            'name': 'Non-Tracking Product',
            'taxable': True,
            'track_stock': False
        }
        
        # Create the product type via the API
        self.product_type_url = reverse('producttype-list') 
        response = self.client.post(self.product_type_url, self.product_type_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        sys.stdout.write("Product Type Created")
        
        self.product_type_id = response.data['id']

        self.category_data = {
            "name": "Test Category",
            "parent": None
        }
        self.category_url = reverse('category-list')
        category_response = self.client.post(self.category_url, self.category_data, format='json')
        self.assertEqual(category_response.status_code, status.HTTP_201_CREATED)
        self.category_id = category_response.data['id']
        

        # Create Product
        self.product_data = {
            "variants_payload": [
                {
                    "is_default_variant": True,
                    "price": "20",
                    "cost_per_unit": "44",
                    "sku": "BBC-3",
                    "color_code": "#FFFFFF",
                    "track_inventory": False,
                }
            ],
            "product_type": self.product_type_id,
            "description": "[{\"type\":\"paragraph\",\"children\":[{\"text\":\"Lorem Ipsum\"}]}]",
            # "tax_class": 1,
            "name": "Titanic",
            "summary": "A ship that sank",
            "images": [
                
            ],
            "meta_title": "423432",
            "meta_description": "234",
            "slug": "giveaway-quiz",
            "status": PublishableStatus.PUBLISHED,
            "category": self.category_id,
            "tags_payload": [
                "sdf",
                "sdfsd"
            ]
        }

        
        self.product_url = reverse('product-list')
        response = self.client.post(self.product_url, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.product_id = response.data['id']



    def tearDown(self):
        # Clean up by logging out after the test
        self.client.logout()
