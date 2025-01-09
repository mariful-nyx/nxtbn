import graphene
from graphene_django.types import DjangoObjectType
from nxtbn.product.models import ProductTranslation, Product
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay

from nxtbn.product.admin_filters import ProductFilter, ProductTranslationFilter

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
    class Meta:
        model = Product
        fields = (
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
    

