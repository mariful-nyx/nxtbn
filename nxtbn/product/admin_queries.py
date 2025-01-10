

import graphene

from graphene_django.filter import DjangoFilterConnectionField
from nxtbn.core.admin_permissions import check_user_permissions
from nxtbn.product.admin_types import CategoryType, CollectionType, ProductGraphType, ProductTagType, ProductTranslationType, ProductVariantType, SupplierType
from nxtbn.product.models import Product, ProductTranslation
from nxtbn.product.storefront_types import CategoryHierarchicalType
from nxtbn.users import UserRole


class ProductTranslationQuery(graphene.ObjectType):
    product = graphene.Field(ProductGraphType, id=graphene.ID(required=True))
    all_products = DjangoFilterConnectionField(ProductGraphType)

    product_translation = graphene.Field(ProductTranslationType, base_product_id=graphene.ID(required=True), lang_code=graphene.String(required=True))
    all_product_translations = DjangoFilterConnectionField(ProductTranslationType)

    all_collections = DjangoFilterConnectionField(CollectionType)
    all_producttags = DjangoFilterConnectionField(ProductTagType)
    all_suppliers = DjangoFilterConnectionField(SupplierType)
    all_product_variants = DjangoFilterConnectionField(ProductVariantType)

    all_categories = DjangoFilterConnectionField(CategoryType)
    hierarchical_categories = DjangoFilterConnectionField(CategoryHierarchicalType)

    def resolve_product(root, info, id):
        check_user_permissions(info, [UserRole.ADMIN, UserRole.STORE_MANAGER, UserRole.PRODUCT_MANAGER, UserRole.MARKETING_MANAGER])

        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None
        
    def resolve_all_products(root, info, **kwargs):
        check_user_permissions(info, [UserRole.ADMIN, UserRole.STORE_MANAGER, UserRole.PRODUCT_MANAGER, UserRole.MARKETING_MANAGER])
        return Product.objects.all()
    
    def resolve_product_translation(root, info, base_product_id, lang_code):
        check_user_permissions(info, [UserRole.ADMIN, UserRole.STORE_MANAGER, UserRole.PRODUCT_MANAGER, UserRole.MARKETING_MANAGER])
        try:
            return ProductTranslation.objects.get(product_id=base_product_id, language_code=lang_code)
        except ProductTranslation.DoesNotExist:
            return None
        
    def resolve_all_product_translations(root, info, **kwargs):
        check_user_permissions(info, [UserRole.ADMIN, UserRole.STORE_MANAGER, UserRole.PRODUCT_MANAGER, UserRole.MARKETING_MANAGER])
        return ProductTranslation.objects.all()