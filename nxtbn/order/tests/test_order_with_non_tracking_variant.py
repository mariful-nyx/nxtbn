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
        
       

    def tearDown(self):
        # Clean up by logging out after the test
        self.client.logout()
