from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.db import transaction
from nxtbn.tax.models import TaxClass, TaxRate


class TaxRateSerializer(serializers.ModelSerializer):
    full_country_name = serializers.SerializerMethodField()

    class Meta:
        model = TaxRate
        ref_name = 'tax_rate_get'
        fields = ('id', 'country', 'full_country_name', 'state', 'rate', 'is_active', )

    def get_full_country_name(self, obj):
        return obj.get_country_display()            
    

class TaxClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxClass
        ref_name = 'tax_class_get'
        fields = '__all__'
    

class TaxClassCreateSerializer(serializers.ModelSerializer):
    tax_rates = TaxRateSerializer(many=True, write_only=True)

    class Meta:
        model = TaxClass
        ref_name = 'tax_class_create'
        fields = ('id', 'name', 'tax_rates',)
        
    def create(self, validated_data):
        tax_rates = validated_data.pop('tax_rates', []) 

        with transaction.atomic():
            instance = TaxClass.objects.create(**validated_data)

            for tax_rate in tax_rates:
                tax_rate = TaxRate.objects.create(tax_class=instance, **tax_rate)
            
            return instance
    

class TaxClassDetailSerializer(serializers.ModelSerializer):
    tax_rates = TaxRateSerializer(many=True, read_only=True)

    class Meta:
        model = TaxClass
        ref_name = 'tax_class_detail_get'
        fields = ('id', 'name', 'tax_rates',)


class TaxClassUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(write_only=True)
    tax_rates = TaxRateSerializer(many=True, write_only=True)

    class Meta:
        model = TaxClass
        ref_name = 'tax_class_update'
        fields = ('id', 'name', 'tax_rates',)

    def update(self, instance, validated_data):
        tax_rates_data = validated_data.pop('tax_rates', [])

        with transaction.atomic():
            instance.name = validated_data.get('name', instance.name)
            instance.save()

            existing_tax_rates = {
                (tax_rate.country, tax_rate.state): tax_rate
                for tax_rate in instance.tax_rates.all()
            }

            new_tax_rate_keys = set()

            for tax_rate_data in tax_rates_data:
                country = tax_rate_data['country']
                state = tax_rate_data.get('state', '')
                new_tax_rate_keys.add((country, state))

                # Update existing tax rate or create a new one
                if (country, state) in existing_tax_rates:
                    tax_rate = existing_tax_rates[(country, state)]
                    for attr, value in tax_rate_data.items():
                        if attr != 'id':  # Ignore 'id' field in updates
                            setattr(tax_rate, attr, value)
                    tax_rate.save()
                else:
                    TaxRate.objects.create(
                        tax_class=instance,
                        country=country,
                        state=state,
                        rate=tax_rate_data['rate'],
                        is_active=tax_rate_data.get('is_active', True)
                    )

            # Remove tax rates that are not in the updated data
            for key in existing_tax_rates.keys() - new_tax_rate_keys:
                existing_tax_rates[key].delete()

        return instance
        