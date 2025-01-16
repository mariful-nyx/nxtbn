import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType
from .models import CurrencyExchange

class CurrencyExchangeType(DjangoObjectType):
    class Meta:
        model = CurrencyExchange
        fields = "__all__"
        interfaces = (relay.Node,)
        filter_fields = {
            'base_currency': ['exact', 'icontains'],
            'target_currency': ['exact', 'icontains'],
            'exchange_rate': ['exact', 'icontains'],
        }
