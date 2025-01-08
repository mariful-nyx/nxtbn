from django.conf import settings
import graphene
from graphene_django import DjangoObjectType
from graphene import relay
from nxtbn.core.utils import apply_exchange_rate
from nxtbn.graph_api.filters import ProductFilter, CategoryFilter, CollectionFilter, ProductTagsFilter
from nxtbn.product.models import Product, Image, Category, ProductVariant, Supplier, ProductType, Collection, ProductTag, TaxClass
from django.utils.translation import get_language


class ImageType(DjangoObjectType):
    class Meta:
        model = Image
        fields = "__all__"

class CategoryType(DjangoObjectType):
    name = graphene.String()

    def resolve_name(self, info):
        if settings.USE_I18N:
            if settings.LANGUAGE_CODE != get_language():
                translation_obj = self.translations.filter(language_code=get_language()).first()
                if translation_obj:
                    return translation_obj.name
        return self.name
    class Meta:
        model = Category
        fields = ("id",)
        interfaces = (relay.Node,)
        filterset_class = CategoryFilter

class SupplierType(DjangoObjectType):
    name = graphene.String()

    def resolve_name(self, info):
        if settings.USE_I18N:
            if settings.LANGUAGE_CODE != get_language():
                translation_obj = self.translations.filter(language_code=get_language()).first()
                if translation_obj:
                    return translation_obj.name
        return self.name
    class Meta:
        model = Supplier
        fields = ("id",)

class ProductTypeType(DjangoObjectType):
    class Meta:
        model = ProductType
        fields = "__all__"

class CollectionType(DjangoObjectType):
    name = graphene.String()

    def resolve_name(self, info):
        if settings.USE_I18N:
            if settings.LANGUAGE_CODE != get_language():
                translation_obj = self.translations.filter(language_code=get_language()).first()
                if translation_obj:
                    return translation_obj.name
        return self.name
    class Meta:
        model = Collection
        fields = ("id",)
        interfaces = (relay.Node,)
        filterset_class = CollectionFilter

class ProductTagType(DjangoObjectType):
    name = graphene.String()

    def resolve_name(self, info):
        if settings.USE_I18N:
            if settings.LANGUAGE_CODE != get_language():
                translation_obj = self.translations.filter(language_code=get_language()).first()
                if translation_obj:
                    return translation_obj.name
        return self.name
    class Meta:
        model = ProductTag
        fields = ("id",)
        interfaces = (relay.Node,)
        filterset_class = ProductTagsFilter

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
    name = graphene.String()
    summary = graphene.String()
    description = graphene.String()
    meta_title = graphene.String()
    meta_description = graphene.String()
    thumbnail = graphene.String()

    def resolve_name(self, info):
        if settings.USE_I18N:
            if settings.LANGUAGE_CODE != get_language():
                translation_obj = self.translations.filter(language_code=get_language()).first()
                if translation_obj:
                    return translation_obj.name
        return self.name
    
    def resolve_summary(self, info):
        if settings.USE_I18N:
            if settings.LANGUAGE_CODE != get_language():
                translation_obj = self.translations.filter(language_code=get_language()).first()
                if translation_obj:
                    return translation_obj.summary
        return self.summary
    
    def resolve_description(self, info):
        if settings.USE_I18N:
            if settings.LANGUAGE_CODE != get_language():
                translation_obj = self.translations.filter(language_code=get_language()).first()
                if translation_obj:
                    return translation_obj.description_html()
        return self.description_html()
    
    def resolve_meta_title(self, info):
        if settings.USE_I18N:
            if settings.LANGUAGE_CODE != get_language():
                translation_obj = self.translations.filter(language_code=get_language()).first()
                if translation_obj:
                    return translation_obj.meta_title
        return self.meta_title
    
    def resolve_meta_description(self, info):
        if settings.USE_I18N:
            if settings.LANGUAGE_CODE != get_language():
                translation_obj = self.translations.filter(language_code=get_language()).first()
                if translation_obj:
                    return translation_obj.meta_description
        return self.meta_description
    
    def resolve_thumbnail(self, info):
        return self.product_thumbnail(info.context)


    class Meta:
        model = Product
        fields = (
            "id",
            "alias",
            "slug",
            "category",
            "brand",
            "related_to",
            "collections",
            "tags",
            "variants",
            "images",
            "default_variant",
        )
        interfaces = (relay.Node,)
        filterset_class = ProductFilter




class CartItemType(graphene.ObjectType):
    product_variant = graphene.Field(ProductVariantType)
    quantity = graphene.Int()
    subtotal = graphene.Float()


class CartType(graphene.ObjectType):
    items = graphene.List(CartItemType)
    total = graphene.String()