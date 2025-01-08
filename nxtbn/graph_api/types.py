import graphene
from graphene_django import DjangoObjectType
from graphene import relay
from nxtbn.core.utils import apply_exchange_rate
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
    price = graphene.String()
    price_without_symbol = graphene.String()
    price_raw = graphene.String()
    
    def resolve_price(self, info): # with currency symbol
        target_currency = info.context.currency
        exchange_rate = info.context.exchange_rate
        converted_price = apply_exchange_rate(self.price, exchange_rate, target_currency, 'en_US')
        return converted_price
    
    def resolve_price_without_symbol(self, info): # without currency symbol
        target_currency = info.context.currency
        exchange_rate = info.context.exchange_rate
        converted_price = apply_exchange_rate(self.price, exchange_rate, target_currency)
        return converted_price
    
    def resolve_price_raw(self, info): # raw price
        return self.price
    class Meta:
        model = ProductVariant
        fields = (
            "id",
            "name",
        )


class ProductGraphType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"
        interfaces = (relay.Node,)
        filterset_class = ProductFilter