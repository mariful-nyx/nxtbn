
from django.test import  TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from nxtbn.users import UserRole
from nxtbn.users.tests import UserFactory


from django.contrib.auth.hashers import make_password

class BaseTestCase(TestCase):
    client = APIClient()
    auth_client = APIClient()
    admin_login_url = reverse('admin_login')
    
    def setUp(self):
        self.user = UserFactory(
            email="test@example.com",
            password=make_password('testpass')
        )       
        
    def permissionDenied(self, request, *args, **kwargs):
        self.assertEqual(request.status_code, 403, *args, **kwargs)

    def requestUnauthorized(self, request, *args, **kwargs):
        self.assertEqual(request.status_code, 401, *args, **kwargs)
        
    def assertSuccess(self, request, *args, **kwargs):
        self.assertEqual(request.status_code, 200, *args, **kwargs)
        
    def loginSeccess(self, login):
        self.assertTrue(login)

    def superAdminLogin(self):
        self.user = UserFactory(
            email="cc@example.com",
            password=make_password('testpass'),
            is_staff=True,
            is_superuser=True,
            role=UserRole.ADMIN
        )
        
        login_data = {
            'email': 'cc@example.com',
            'password': 'testpass'
        }
        
        response = self.client.post(self.admin_login_url, login_data)
        self.assertSuccess(response)
       
        access_token = response.data['token']['access']
        
        self.auth_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def adminLogin(self):
       
        self.user = UserFactory(
            email="cc@example.com",
            password=make_password('testpass'),
            is_staff=True,
            role=UserRole.ADMIN
        )

        login_data = {
            'email': 'cc@example.com',
            'password': 'testpass'
        }
        
        response = self.client.post(self.admin_login_url, login_data)
        self.assertSuccess(response)
       
        access_token = response.data['token']['access']
        
        self.auth_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
    def customerLogin(self):
      
        self.user = UserFactory(
            email="cc@example.com",
            password=make_password('testpass'),
            role=UserRole.CUSTOMER,
            is_staff=False
        )
        login_data = {
            'email': 'cc@example.com',
            'password': 'testpass'
        }
        
        response = self.client.post(self.admin_login_url, login_data)
        self.assertSuccess(response)
       
        access_token = response.data['token']['access']
        
        self.auth_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def storeManagerLogin(self):
       
        self.user = UserFactory(
            email="cc@example.com",
            password=make_password('testpass'),
            role=UserRole.STORE_MANAGER,
            is_staff=False
        )
        login_data = {
            'email': 'cc@example.com',
            'password': 'testpass'
        }
        self.admin_login_url = reverse('admin_login')
        response = self.client.post(self.admin_login_url, login_data)
        self.assertSuccess(response)
           
        access_token = response.data['token']['access']
        
        self.auth_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    
    def marketingManagerLogin(self):
        self.user = UserFactory(
            email="cc@example.com",
            password=make_password('testpass'),
            role=UserRole.STORE_MANAGER,
            is_staff=False
        )
        login_data = {
            'email': 'cc@example.com',
            'password': 'testpass'
        }
        self.admin_login_url = reverse('admin_login')
        response = self.client.post(self.admin_login_url, login_data)
        self.assertSuccess(response)
           
        access_token = response.data['token']['access']
        
        self.auth_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

