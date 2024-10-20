from rest_framework import serializers

from nxtbn.shipping.models import ShippingMethod, ShippingRate

class ShippingRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingRate
        fields = [
            'id', 
            'shipping_method',
            'country',
            'region', 
            'city', 
            'weight_min', 
            'weight_max', 
            'rate', 
            'incremental_rate', 
        ]
        
        extra_kwargs = {
            'shipping_method': {'write_only': True},
            'region': {'required': False, 'allow_null': True},
            'city': {'required': False, 'allow_null': True}
        }

class ShippingMethodSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    class Meta:
        model = ShippingMethod
        fields = ['id', 'name', 'description', 'carrier', 'label', 'value']

    def get_label(self, instance):
        return f"{instance.name} - {instance.carrier}"
    
    def get_value(self, instance):
        return instance.id
    

class ShppingMethodDetailSeralizer(serializers.ModelSerializer):
    rates = ShippingRateSerializer(read_only=True, many=True)

    class Meta:
        model = ShippingMethod
        fields = ['id', 'name', 'description', 'carrier', 'rates']