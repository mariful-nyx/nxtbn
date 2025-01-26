

import graphene

from graphene_django.filter import DjangoFilterConnectionField
from nxtbn.core.admin_permissions import check_user_permissions
from nxtbn.product.admin_types import CategoryTranslationType, CategoryType, CollectionTranslationType, CollectionType, ProductGraphType, ProductTagTranslationType, ProductTagType, ProductTranslationType, ProductVariantAdminType, SupplierType
from nxtbn.product.models import Category, CategoryTranslation, Collection, CollectionTranslation, Product, ProductTag, ProductTagTranslation, ProductTranslation, Supplier
from nxtbn.users import UserRole


class ProductQuery(graphene.ObjectType):
    product = graphene.Field(ProductGraphType, id=graphene.ID(required=True))
    products = DjangoFilterConnectionField(ProductGraphType)

    

    collection = graphene.Field(CollectionType, id=graphene.ID(required=True))
    collections = DjangoFilterConnectionField(CollectionType)

    producttag = graphene.Field(ProductTagType, id=graphene.ID(required=True))
    producttags = DjangoFilterConnectionField(ProductTagType)

    supplier = graphene.Field(SupplierType, id=graphene.ID(required=True))
    suppliers = DjangoFilterConnectionField(SupplierType)
    product_variants = DjangoFilterConnectionField(ProductVariantAdminType)

    category = graphene.Field(CategoryType, id=graphene.ID(required=True))
    categories = DjangoFilterConnectionField(CategoryType)
    category = graphene.Field(CategoryType, id=graphene.ID(required=True))

    # All translations

    product_translation = graphene.Field(ProductTranslationType, base_product_id=graphene.ID(required=True), lang_code=graphene.String(required=True))
    product_translations = DjangoFilterConnectionField(ProductTranslationType)

    category_translation = graphene.Field(CategoryTranslationType, base_category_id=graphene.ID(required=True), lang_code=graphene.String(required=True))
    category_translations = DjangoFilterConnectionField(CategoryTranslationType)

    collection_translation = graphene.Field(CollectionTranslationType, base_collection_id=graphene.ID(required=True), lang_code=graphene.String(required=True))
    collection_translations = DjangoFilterConnectionField(CollectionTranslationType)

    producttags_translation = graphene.Field(ProductTagTranslationType, base_tag_id=graphene.ID(required=True), lang_code=graphene.String(required=True))
    tags_translations = DjangoFilterConnectionField(ProductTagTranslationType)

 
    def resolve_product(root, info, id):
        check_user_permissions(info, any_staff=True)

        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None
        
    def resolve_products(root, info, **kwargs):
        check_user_permissions(info, any_staff=True)
        return Product.objects.all()
    
    def resolve_collection(root, info, id):
        check_user_permissions(info, any_staff=True)

        try:
            return Collection.objects.get(pk=id)
        except Collection.DoesNotExist:
            return None
    
    def resolve_collections(root, info, **kwargs):
        check_user_permissions(info, any_staff=True)
        return Collection.objects.all()
    
    def resolve_producttag(root, info, id):
        check_user_permissions(info, any_staff=True)

        try:
            return ProductTag.objects.get(pk=id)
        except ProductTag.DoesNotExist:
            return None
        
    def resolve_producttags(root, info, **kwargs):
        check_user_permissions(info, any_staff=True)
        return ProductTag.objects.all()
    
    def resolve_supplier(root, info, id):
        check_user_permissions(info, any_staff=True)

        try:
            return Supplier.objects.get(pk=id)
        except Supplier.DoesNotExist:
            return None
    
    def resolve_suppliers(root, info, **kwargs):
        check_user_permissions(info, any_staff=True)
        return Product.objects.all()
    
    def resolve_product_variants(root, info, **kwargs):
        check_user_permissions(info, any_staff=True)
        return Product.objects.all()
    
    def resolve_category(root, info, id):
        check_user_permissions(info, any_staff=True)

        try:
            return Category.objects.get(pk=id)
        except Category.DoesNotExist:
            return None
        
    # All translations

    def resolve_category_translation(root, info, base_category_id, lang_code):
        check_user_permissions(info, any_staff=True)
        try:
            return CategoryTranslation.objects.get(category_id=base_category_id, language_code=lang_code)
        except CategoryTranslation.DoesNotExist:
            return None
        
    def resolve_category_translations(root, info, **kwargs):
        check_user_permissions(info, any_staff=True)
        return CategoryTranslation.objects.all()
    
    def resolve_collection_translation(root, info, base_collection_id, lang_code):
        check_user_permissions(info, any_staff=True)
        try:
            return CollectionTranslation.objects.get(collection_id=base_collection_id, language_code=lang_code)
        except CollectionTranslation.DoesNotExist:
            return None
        
    def resolve_collection_translations(root, info, **kwargs):
        check_user_permissions(info, any_staff=True)
        return CollectionTranslation.objects.all()
    
    def resolve_tags_translation(root, info, base_tag_id, lang_code):
        check_user_permissions(info, any_staff=True)
        try:
            return ProductTagTranslation.objects.get(tag_id=base_tag_id, language_code=lang_code)
        except ProductTagTranslation.DoesNotExist:
            return None
        
    def resolve_tags_translations(root, info, **kwargs):
        check_user_permissions(info, any_staff=True)
        return ProductTagTranslation.objects.all()

    
    def resolve_product_translation(root, info, base_product_id, lang_code):
        check_user_permissions(info, any_staff=True)
        try:
            return ProductTranslation.objects.get(product_id=base_product_id, language_code=lang_code)
        except ProductTranslation.DoesNotExist:
            return None
        
    def resolve_product_translations(root, info, **kwargs):
        check_user_permissions(info, any_staff=True)
        return ProductTranslation.objects.all()
    
