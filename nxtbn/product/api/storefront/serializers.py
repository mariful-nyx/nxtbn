from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.db import transaction

from nxtbn.core.models import CurrencyExchange
from nxtbn.core.utils import apply_exchange_rate, get_in_user_currency
from nxtbn.product.api.dashboard.serializers import RecursiveCategorySerializer
from nxtbn.filemanager.api.dashboard.serializers import ImageSerializer
from nxtbn.product.models import Product, Collection, Category, ProductVariant

from nxtbn.core.currency.backend import currency_Backend

class CategorySerializer(RecursiveCategorySerializer):
    pass

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'name', 'description', 'is_active', 'image',)


class ProductVariantSerializer(serializers.ModelSerializer):
    variant_image = ImageSerializer(read_only=True)
    price = serializers.SerializerMethodField()
    class Meta:
        model = ProductVariant
        fields = '__all__'
 
    def get_price(self, obj):
        target_currency = self.context['request'].currency
        converted_price = apply_exchange_rate(obj.price, self.context['exchange_rate'], target_currency, 'en_US')
        return converted_price

class ProductWithVariantSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True)
    product_thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'summary',
            'description',
            'category',
            'brand',
            'slug',
            'variants',
            'product_thumbnail'
        )

    def get_product_thumbnail(self, obj):
        return obj.product_thumbnail(self.context['request'])
    

class ProductWithDefaultVariantSerializer(serializers.ModelSerializer):
    product_thumbnail = serializers.SerializerMethodField()
    default_variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'summary',
            'description',
            'category',
            'brand',
            'slug',
            'default_variant',
            'product_thumbnail'
        )

    def get_product_thumbnail(self, obj):
        return obj.product_thumbnail(self.context['request'])


class ProductDetailSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True)
    default_variant = ProductVariantSerializer(read_only=True)
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'summary',
            'description',
            'brand',
            'category',
            'collections',
            'images',
            'created_by',
            'default_variant',
            'variants',
        )