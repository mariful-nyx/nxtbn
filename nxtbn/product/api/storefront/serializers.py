from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.db import transaction

from nxtbn.core.models import CurrencyExchange
from nxtbn.product.api.dashboard.serializers import RecursiveCategorySerializer
from nxtbn.filemanager.api.dashboard.serializers import ImageSerializer
from nxtbn.product.models import Product, Collection, Category, ProductVariant


class CategorySerializer(RecursiveCategorySerializer):
    pass

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'name', 'description', 'is_active', 'image',)


class ProductVariantSerializer(serializers.ModelSerializer):
    variant_image = ImageSerializer(many=True, read_only=True)
    price_in_customer_currency = serializers.SerializerMethodField()
    class Meta:
        model = ProductVariant
        fields = '__all__'

    def get_price_in_customer_currency(self, obj): # TODO: Implement logic for taxclass in future
        if not settings.IS_MULTI_CURRENCY: # If site is in single currency, no conversion required
            return obj.price
        else:
            from nxtbn.core.currency.utils import currency_Backend
            currency_code = self.context.get('request').currency
            rate = currency_Backend().convert_to_customer_currency(currency_code, obj.price)
        return rate

class ProductSerializer(serializers.ModelSerializer):
    default_variant = ProductVariantSerializer()
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'summary',
            'description',
            'category',
            'brand',
            'type',
            'currency',
            'slug',
            'default_variant',
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True)
    default_variant = ProductVariantSerializer()
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'summary',
            'description',
            'brand',
            'type',
            'currency',
            'category',
            'collections',
            'media',
            'created_by',
            'default_variant',
            'variants',
        )