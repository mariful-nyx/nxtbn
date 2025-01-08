
from django.test import  TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from nxtbn.users import UserRole
from nxtbn.users.tests import UserFactory
from django.test import TestCase
from graphene.test import Client as GRAPHClient
from django.contrib.auth.hashers import make_password
from nxtbn.storefront_schema import storefront_schema
from nxtbn.users import UserRole
from nxtbn.users.tests import UserFactory

from django.contrib.auth.hashers import make_password




class BaseTestCase(TestCase):
    client = GRAPHClient(storefront_schema)
    auth_client = None  # This will hold the authenticated client

    def setUp(self):
        self.user = UserFactory(
            email="test@example.com",
            password=make_password('testpass')
        )

    def assertGraphQLResponse(self, response, expected_status):
        """Check the status of the GraphQL response."""
        self.assertIn('errors', response if expected_status != 200 else {})
        self.assertIn('data', response if expected_status == 200 else {})
        if expected_status != 200:
            self.assertEqual(response.get('errors', [{}])[0].get('message'), 'Unauthorized')

    def superAdminLogin(self):
        self.user = UserFactory(
            email="cc@example.com",
            password=make_password('testpass'),
            is_staff=True,
            is_superuser=True,
            role=UserRole.ADMIN
        )
        
        login_mutation = """
        mutation AdminLogin($email: String!, $password: String!) {
            tokenAuth(email: $email, password: $password) {
                token
            }
        }
        """
        
        variables = {'email': 'cc@example.com', 'password': 'testpass'}
        response = self.client.execute(login_mutation, variables=variables)
        self.assertGraphQLResponse(response, 200)

        token = response['data']['tokenAuth']['token']
        self.auth_client = GRAPHClient(storefront_schema, headers={"Authorization": f"Bearer {token}"})

    def adminLogin(self):
        self.user = UserFactory(
            email="cc@example.com",
            password=make_password('testpass'),
            is_staff=True,
            role=UserRole.ADMIN
        )
        
        login_mutation = """
        mutation AdminLogin($email: String!, $password: String!) {
            tokenAuth(email: $email, password: $password) {
                token
            }
        }
        """
        
        variables = {'email': 'cc@example.com', 'password': 'testpass'}
        response = self.client.execute(login_mutation, variables=variables)
        self.assertGraphQLResponse(response, 200)

        token = response['data']['tokenAuth']['token']
        self.auth_client = GRAPHClient(storefront_schema, headers={"Authorization": f"Bearer {token}"})

    def customerLogin(self):
        self.user = UserFactory(
            email="cc@example.com",
            password=make_password('testpass'),
            role=UserRole.CUSTOMER,
            is_staff=False,
            is_superuser=False
        )
        
        login_mutation = """
        mutation CustomerLogin($email: String!, $password: String!) {
            tokenAuth(email: $email, password: $password) {
                token
            }
        }
        """
        
        variables = {'email': 'cc@example.com', 'password': 'testpass'}
        response = self.client.execute(login_mutation, variables=variables)
        self.assertGraphQLResponse(response, 200)

        token = response['data']['tokenAuth']['token']
        self.auth_client = GRAPHClient(storefront_schema, headers={"Authorization": f"Bearer {token}"})

    def storeManagerLogin(self):
        self.user = UserFactory(
            email="cc@example.com",
            password=make_password('testpass'),
            role=UserRole.STORE_MANAGER,
            is_staff=False
        )
        
        login_mutation = """
        mutation StoreManagerLogin($email: String!, $password: String!) {
            tokenAuth(email: $email, password: $password) {
                token
            }
        }
        """
        
        variables = {'email': 'cc@example.com', 'password': 'testpass'}
        response = self.client.execute(login_mutation, variables=variables)
        self.assertGraphQLResponse(response, 200)

        token = response['data']['tokenAuth']['token']
        self.auth_client = GRAPHClient(storefront_schema, headers={"Authorization": f"Bearer {token}"})

    def marketingManagerLogin(self):
        self.user = UserFactory(
            email="cc@example.com",
            password=make_password('testpass'),
            role=UserRole.STORE_MANAGER,
            is_staff=False
        )
        
        login_mutation = """
        mutation MarketingManagerLogin($email: String!, $password: String!) {
            tokenAuth(email: $email, password: $password) {
                token
            }
        }
        """
        
        variables = {'email': 'cc@example.com', 'password': 'testpass'}
        response = self.client.execute(login_mutation, variables=variables)
        self.assertGraphQLResponse(response, 200)

        token = response['data']['tokenAuth']['token']
        self.auth_client = GRAPHClient(storefront_schema, headers={"Authorization": f"Bearer {token}"})


class BaseTestCase(TestCase):
    client = APIClient()
    auth_client = APIClient()
    admin_login_url = reverse('admin_login')
    customer_login_url = reverse('customer_login')
    
    def setUp(self):
        self.user = UserFactory(
            email="test@example.com",
            password=make_password('testpass')
        )       
        
    def badRequest(self, request, *args, **kwargs):
        self.assertEqual(request.status_code, 400, *args, **kwargs)

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
            is_staff=False,
            is_superuser=False
        )
        login_data = {
            'email': 'cc@example.com',
            'password': 'testpass'
        }
        
        response = self.client.post(self.customer_login_url, login_data)
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




