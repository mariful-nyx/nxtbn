from rest_framework import serializers

from nxtbn.shipping.models import ShippingMethod, ShippingRate

class ShippingMethodSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    class Meta:
        model = ShippingMethod
        fields = ['id', 'name', 'carrier', 'label', 'value']

    def get_label(self, instance):
        return f"{instance.name} - {instance.carrier}"
    
    def get_value(self, instance):
        return instance.id