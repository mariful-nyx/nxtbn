import graphene

from nxtbn.core.admin_types import CurrencyExchangeType
from nxtbn.core.models import CurrencyExchange
from graphene_django.filter import DjangoFilterConnectionField


class AdminCoreQuery(graphene.ObjectType):
    all_currency_exchange = DjangoFilterConnectionField(CurrencyExchangeType)
    currency_exchanges = graphene.Field(CurrencyExchangeType, id=graphene.ID(required=True))

    def resolve_all_currency_exchange(self, info, **kwargs):
        return CurrencyExchange.objects.all()
    
    def resolve_currency_exchanges(self, info, id):
        try:
            return CurrencyExchange.objects.get(id=id)
        except CurrencyExchange.DoesNotExist:
            return None