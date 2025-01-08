from django.test import TestCase
from nxtbn.core import PublishableStatus
from nxtbn.home.base_tests import BaseGraphQLTestCase
from nxtbn.product.models import Product, Category, Collection, ProductTag
from nxtbn.product.tests import (
    ProductFactory,
    CategoryFactory,
    CollectionFactory,
    ProductTagFactory,
)
from nxtbn.admin_schema import admin_schema
from graphene.test import Client as GRAPHClient

class ProductQueryTestCase(BaseGraphQLTestCase):
    def setUp(self):
        super().setUp()

        # Create sample data for testing
        self.category = CategoryFactory(name="Test Category")
        self.collection = CollectionFactory(name="Test Collection")
        self.tag = ProductTagFactory(name="Test Tag")
        self.product = ProductFactory(
            name="Test Product",
            category=self.category,
            # collections=[self.collection],
            # tags=[self.tag],
            status=PublishableStatus.PUBLISHED,
        )

    def test_resolve_product_valid_id(self):
        query = """
        query getProduct($id: ID!) {
            product(id: $id) {
                id
                name
                category {
                    name
                }
            }
        }
        """

        variables = {"id": self.product.id}
        response = self.graphql_customer_client.execute(query, variables=variables)


        self.assertGraphQLSuccess(response)
        data = response["data"]["product"]

        self.assertEqual(data["name"], "Test Product")
        self.assertEqual(data["category"]["name"], "Test Category")

    def test_resolve_product_invalid_id(self):
        query = """
        query getProduct($id: ID!) {
            product(id: $id) {
                id
            }
        }
        """

        variables = {"id": "invalid-id"}
        response = self.graphql_customer_client.execute(query, variables=variables)

        self.assertGraphQLFailure(response)
        self.assertIsNone(response["data"]["product"])  # Product should be None

    def test_resolve_all_products(self):
        query = """
        query getAllProducts {
            allProducts {
                edges {
                    node {
                        id
                        name
                        category {
                            name
                        }
                    }
                }
            }
        }
        """

        response = self.graphql_customer_client.execute(query)

        self.assertGraphQLSuccess(response)
        products = response["data"]["allProducts"]["edges"]

        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["node"]["name"], "Test Product")
        self.assertEqual(products[0]["node"]["category"]["name"], "Test Category")

    def test_resolve_all_categories(self):
        query = """
        query getAllCategories {
            allCategories {
                edges {
                    node {
                        id
                        name
                    }
                }
            }
        }
        """

        response = self.graphql_customer_client.execute(query)

        # self.assertGraphQLSuccess(response, expected_status=200)
        # categories = response["data"]["allCategories"]["edges"]

        # self.assertEqual(len(categories), 1)
        # self.assertEqual(categories[0]["node"]["name"], "Test Category")

    def test_resolve_all_collections(self):
        query = """
        query getAllCollections {
            allCollections {
                edges {
                    node {
                        id
                        name
                    }
                }
            }
        }
        """

        response = self.graphql_customer_client.execute(query)

        # self.assertGraphQLSuccess(response, expected_status=200)
        # collections = response["data"]["allCollections"]["edges"]

        # self.assertEqual(len(collections), 1)
        # self.assertEqual(collections[0]["node"]["name"], "Test Collection")

    def test_resolve_all_tags(self):
        query = """
        query getAllTags {
            allTags {
                edges {
                    node {
                        id
                        name
                    }
                }
            }
        }
        """

        response = self.graphql_customer_client.execute(query)

        # self.assertGraphQLSuccess(response, expected_status=200)
        # tags = response["data"]["allTags"]["edges"]

        # self.assertEqual(len(tags), 1)
        # self.assertEqual(tags[0]["node"]["name"], "Test Tag")
