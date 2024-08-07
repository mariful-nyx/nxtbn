from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.db import transaction

from nxtbn.filemanager.api.dashboard.serializers import ImageSerializer
from nxtbn.product.models import Color, Product, Category, Collection, ProductTag, ProductType, ProductVariant

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'parent', 'subcategories',)
        read_only_fields = ('subcategories',)
        ref_name = 'category_dashboard_get'

class NameIDCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)

class BasicCategorySerializer(serializers.ModelSerializer):
    parent = NameIDCategorySerializer(read_only=True)
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'parent', 'has_sub')
        read_only_fields = ('subcategories',)
        ref_name = 'category_dashboard_basic'

class RecursiveCategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'children')

    def get_children(self, obj):
        children = obj.subcategories.all()
        return RecursiveCategorySerializer(children, many=True).data

class CollectionSerializer(serializers.ModelSerializer):
    images_details = ImageSerializer(read_only=True, source='image')
    class Meta:
        model = Collection
        fields = (
            'id',
            'name',
            'description',
            'is_active',
            'image',
            'images_details',
        )
        ref_name = 'collection_dashboard_get'
        write_only_fields = ('image',)

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        ref_name = 'product_variant_dashboard_get'
        fields = ('id', 'product', 'name', 'compare_at_price', 'price', 'cost_per_unit', 'sku',)

class ProductSerializer(serializers.ModelSerializer):
    default_variant = ProductVariantSerializer(read_only=True)
    product_thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Product 
        ref_name = 'product_dashboard_get'
        fields =  (
            'id',
            'name',
            'summary',
            'description',
            'images',
            'category',
            'supplier',
            'brand',
            'product_type',
            'related_to',
            'default_variant',
            'collections',
            'product_thumbnail',
            'colors',
        )
    
    def get_product_thumbnail(self, obj):
        return obj.product_thumbnail(self.context['request'])

class ProductDetailsSerializer(serializers.ModelSerializer):
    default_variant = ProductVariantSerializer(read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product 
        ref_name = 'product_dashboard_get'
        fields =  (
            'id',
            'slug',
            'name',
            'summary',
            'description',
            'images',
            'category',
            'supplier',
            'brand',
            'product_type',
            'related_to',
            'default_variant',
            'collections',
            'colors',
            'meta_title',
            'meta_description',
        )
    

class VariantCreatePayloadSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)
    compare_at_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    cost_per_unit = serializers.DecimalField(max_digits=10, decimal_places=2)
    sku = serializers.CharField(max_length=255, required=False)
    stock = serializers.IntegerField(required=False)
    weight_unit = serializers.CharField(max_length=10, required=False)
    weight_value = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    color_code = serializers.CharField(max_length=7, required=False)

class ProductCreateSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    variants_payload = VariantCreatePayloadSerializer(many=True, write_only=True)
    currency = serializers.CharField(max_length=3, required=False, write_only=True)
    class Meta:
        model = Product
        ref_name = 'product_dashboard_create'
        fields =  (
            'id',
            'slug',
            'name',
            'summary',
            'description',
            'images',
            'category',
            'supplier',
            'brand',
            'product_type',
            'related_to',
            'default_variant',
            'variants',
            'collections',

            # write only fields
            'variants_payload',
            'currency',
            'meta_title',
            'meta_description',
        )


    def create(self, validated_data):
        collection = validated_data.pop('collections', [])
        images = validated_data.pop('images', [])
        variants_payload = validated_data.pop('variants_payload', [])
        currency = validated_data.pop('currency', 'USD')

        instance = Product.objects.create(
            **validated_data,
            **{'created_by': self.context['request'].user}
        )

        instance.collections.set(collection)
        instance.images.set(images)

        # Create variants and set the first one as the default variant
        default_variant = None
        for i, variant_payload in enumerate(variants_payload):
            variant = ProductVariant.objects.create(
                product=instance,
                currency=currency,
                **variant_payload
            )
            if i == 0:
                default_variant = variant

        if default_variant:
            instance.default_variant = default_variant
            instance.save()
        
        return instance
    

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

    
class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'

class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = '__all__'

        