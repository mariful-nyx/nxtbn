

import graphene

from graphene_django.filter import DjangoFilterConnectionField
from nxtbn.core.admin_permissions import check_user_permissions
from nxtbn.product.admin_types import CategoryTranslationType, CategoryType, CollectionTranslationType, CollectionType, ProductGraphType, ProductTagTranslationType, ProductTagType, ProductTranslationType, ProductVariantType, SupplierType
from nxtbn.product.models import CategoryTranslation, CollectionTranslation, Product, ProductTagTranslation, ProductTranslation
from nxtbn.product.storefront_types import CategoryHierarchicalType
from nxtbn.users import UserRole


class ProductQuery(graphene.ObjectType):
    product = graphene.Field(ProductGraphType, id=graphene.ID(required=True))
    all_products = DjangoFilterConnectionField(ProductGraphType)

    

    all_collections = DjangoFilterConnectionField(CollectionType)
    all_producttags = DjangoFilterConnectionField(ProductTagType)
    all_suppliers = DjangoFilterConnectionField(SupplierType)
    all_product_variants = DjangoFilterConnectionField(ProductVariantType)

    all_categories = DjangoFilterConnectionField(CategoryType)
    hierarchical_categories = DjangoFilterConnectionField(CategoryHierarchicalType)

    # All translations

    product_translation = graphene.Field(ProductTranslationType, base_product_id=graphene.ID(required=True), lang_code=graphene.String(required=True))
    all_product_translations = DjangoFilterConnectionField(ProductTranslationType)

    category_translation = graphene.Field(CategoryTranslationType, base_category_id=graphene.ID(required=True), lang_code=graphene.String(required=True))
    all_category_translations = DjangoFilterConnectionField(CategoryTranslationType)

    collection_translation = graphene.Field(CollectionTranslationType, base_collection_id=graphene.ID(required=True), lang_code=graphene.String(required=True))
    all_collection_translations = DjangoFilterConnectionField(CollectionTranslationType)

    tags_translation = graphene.Field(ProductTagTranslationType, base_tag_id=graphene.ID(required=True), lang_code=graphene.String(required=True))
    all_tags_translations = DjangoFilterConnectionField(ProductTagTranslationType)

 

    def resolve_category_translation(root, info, base_category_id, lang_code):
        check_user_permissions(info, any_staff=True)
        try:
            return CategoryTranslation.objects.get(category_id=base_category_id, language_code=lang_code)
        except CategoryTranslation.DoesNotExist:
            return None
        
    def resolve_all_category_translations(root, info, **kwargs):
        check_user_permissions(info, any_staff=True)
        return CategoryTranslation.objects.all()
    
    def resolve_collection_translation(root, info, base_collection_id, lang_code):
        check_user_permissions(info, any_staff=True)
        try:
            return CollectionTranslation.objects.get(collection_id=base_collection_id, language_code=lang_code)
        except CollectionTranslation.DoesNotExist:
            return None
        
    def resolve_all_collection_translations(root, info, **kwargs):
        check_user_permissions(info, any_staff=True)
        return CollectionTranslation.objects.all()
    
    def resolve_tags_translation(root, info, base_tag_id, lang_code):
        check_user_permissions(info, any_staff=True)
        try:
            return ProductTagTranslation.objects.get(tag_id=base_tag_id, language_code=lang_code)
        except ProductTagTranslation.DoesNotExist:
            return None
        
    def resolve_all_tags_translations(root, info, **kwargs):
        check_user_permissions(info, any_staff=True)
        return ProductTagTranslation.objects.all()


    def resolve_product(root, info, id):
        check_user_permissions(info, any_staff=True)

        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None
        
    def resolve_all_products(root, info, **kwargs):
        check_user_permissions(info, any_staff=True)
        return Product.objects.all()
    
    def resolve_product_translation(root, info, base_product_id, lang_code):
        check_user_permissions(info, any_staff=True)
        try:
            return ProductTranslation.objects.get(product_id=base_product_id, language_code=lang_code)
        except ProductTranslation.DoesNotExist:
            return None
        
    def resolve_all_product_translations(root, info, **kwargs):
        check_user_permissions(info, any_staff=True)
        return ProductTranslation.objects.all()