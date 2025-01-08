import graphene
from nxtbn.core import PublishableStatus
from nxtbn.graph_api.types import (
    ProductGraphType,
    ImageType,
    CategoryType,
    SupplierType,
    ProductTypeType,
    CollectionType,
    ProductTagType,
    TaxClassType,
)
from nxtbn.product.models import Product, Image, Category, Supplier, ProductType, Collection, ProductTag, TaxClass
from graphene_django.filter import DjangoFilterConnectionField




class Query(graphene.ObjectType):
    product = graphene.Field(ProductGraphType, id=graphene.ID(required=True))
    all_products = DjangoFilterConnectionField(ProductGraphType)

    def resolve_product(root, info, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None

    def resolve_all_products(root, info, **kwargs):
        return Product.objects.filter(
            status=PublishableStatus.PUBLISHED
        )

schema = graphene.Schema(query=Query)
