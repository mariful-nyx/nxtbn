import graphene
from graphene_django.types import DjangoObjectType
from nxtbn.product.models import Category, Collection, ProductTag, ProductTranslation, Product, ProductVariant, Supplier
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay

from nxtbn.product.admin_filters import CategoryFilter, CollectionFilter, ProductFilter, ProductTagsFilter, ProductTranslationFilter
from nxtbn.product.storefront_filters import ProductVariantFilter, SupplierFilter

class ProductTranslationType(DjangoObjectType):
    description_html = graphene.String()
    base_product_id = graphene.Int()
    class Meta:
        model = ProductTranslation
        fields = (
            'name',
            'summary',
            'description',
            'language_code',
            'meta_title',
            'meta_description',
        )
        interfaces = (relay.Node,)
        filterset_class = ProductTranslationFilter

    def resolve_description_html(self, info):
        return self.description_html()
    
    def resolve_base_product_id(self, info):
        return self.product_id

class ProductGraphType(DjangoObjectType):
    description_html = graphene.String()
    db_id = graphene.Int(source="id")
    class Meta:
        model = Product
        fields = (
            'id',
            'slug',
            'name',
            'name_when_in_relation',
            'summary',
            'description',
            'images',
            'category',
            'supplier',
            'brand',
            'product_type',
            'default_variant',
            'collections',
            'tags',
            'tax_class',
            'related_to',
            'meta_title',
            'meta_description',
        )

        interfaces = (relay.Node,)
        filterset_class = ProductFilter

    def resolve_description_html(self, info):
        return self.description_html()
    

class CollectionType(DjangoObjectType):
    db_id = graphene.Int(source="id")
    class Meta:
        model = Collection
        fields = (
            'name',
            'slug',
            'description',
            'meta_title',
            'meta_description',
            'image',
            'products',
        )
        interfaces = (relay.Node,)
        filterset_class = CollectionFilter


class CategoryType(DjangoObjectType):
    db_id = graphene.Int(source="id")
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
            'description',
            'meta_title',
            'meta_description',
        )
        interfaces = (relay.Node,)
        filterset_class = CategoryFilter


class ProductTagType(DjangoObjectType):
    db_id = graphene.Int(source="id")
    class Meta:
        model = ProductTag
        fields = (
            'name',
        )
        interfaces = (relay.Node,)
        filterset_class = ProductTagsFilter


class SupplierType(DjangoObjectType):
    db_id = graphene.Int(source="id")
    class Meta:
        model = Supplier
        fields = (
            'name',
            'slug',
            'description',
            'meta_title',
            'meta_description',
            'image',
            'products',
        )
        interfaces = (relay.Node,)
        filterset_class = SupplierFilter

class ProductVariantType(DjangoObjectType):
    db_id = graphene.Int(source="id")
    class Meta:
        model = ProductVariant
        fields = (
            'name',
            'sku',
            'track_inventory',
            'quantity',
            'cost_price',
            'images',
            'weight',
            'weight_unit',
            'product',
            'attributes',
            'price',
        )
        interfaces = (relay.Node,)
        filterset_class = ProductVariantFilter






class CategoryHierarchicalType(DjangoObjectType):
    db_id = graphene.Int(source="id")
    name = graphene.String()
    description = graphene.String()
    meta_title = graphene.String()
    meta_description = graphene.String()

    # Recursive field for subcategories
    children = graphene.List(lambda: CategoryHierarchicalType)
    
    def resolve_children(self, info):
        return self.subcategories.all()
    
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'description',
            'meta_title',
            'meta_description',
            'children',
        )
        interfaces = (relay.Node,)
        filterset_class = CategoryFilter