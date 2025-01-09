

import graphene

from graphene_django.filter import DjangoFilterConnectionField
from nxtbn.product.admin_types import ProductGraphType, ProductTranslationType
from nxtbn.product.models import Product, ProductTranslation


class ProductTranslationQuery(graphene.ObjectType):
    product = graphene.Field(ProductGraphType, id=graphene.ID(required=True))
    all_products = DjangoFilterConnectionField(ProductGraphType)

    product_translation = graphene.Field(ProductTranslationType, base_product_id=graphene.ID(required=True), lang_code=graphene.String(required=True))
    all_product_translations = DjangoFilterConnectionField(ProductTranslationType)

    def resolve_product(root, info, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None
        
    def resolve_all_products(root, info, **kwargs):
        return Product.objects.all()
    
    def resolve_product_translation(root, info, base_product_id, lang_code):
        try:
            return ProductTranslation.objects.get(product_id=base_product_id, language_code=lang_code)
        except ProductTranslation.DoesNotExist:
            return None
        
    def resolve_all_product_translations(root, info, **kwargs):
        return ProductTranslation.objects.all()