import graphene
from graphene_django import DjangoObjectType
from graphene import relay
from nxtbn.graph_api.filters import ProductFilter
from nxtbn.product.models import Product, Image, Category, ProductVariant, Supplier, ProductType, Collection, ProductTag, TaxClass

class ImageType(DjangoObjectType):
    class Meta:
        model = Image
        fields = "__all__"

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"

class SupplierType(DjangoObjectType):
    class Meta:
        model = Supplier
        fields = "__all__"

class ProductTypeType(DjangoObjectType):
    class Meta:
        model = ProductType
        fields = "__all__"

class CollectionType(DjangoObjectType):
    class Meta:
        model = Collection
        fields = "__all__"

class ProductTagType(DjangoObjectType):
    class Meta:
        model = ProductTag
        fields = "__all__"

class TaxClassType(DjangoObjectType):
    class Meta:
        model = TaxClass
        fields = "__all__"

class ProductVariantType(DjangoObjectType):
    class Meta:
        model = ProductVariant
        fields = '__all__'
        interfaces = (relay.Node,)

class ProductGraphType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"
        interfaces = (relay.Node,)
        filterset_class = ProductFilter

    def resolve_category(self, info):
        return self.category

