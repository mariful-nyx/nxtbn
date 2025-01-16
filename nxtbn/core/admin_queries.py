import graphene

from nxtbn.core.admin_types import CurrencyExchangeType
from nxtbn.core.models import CurrencyExchange
from graphene_django.filter import DjangoFilterConnectionField


class CoreQuery(graphene.ObjectType):
    currency_exchanges = DjangoFilterConnectionField(CurrencyExchangeType)
    currency_exchange = graphene.Field(CurrencyExchangeType, id=graphene.ID(required=True))

    def resolve_currency_exchanges(self, info):
        return CurrencyExchange.objects.all()

    def resolve_currency_exchange(self, info, id):
        try:
            return CurrencyExchange.objects.get(pk=id)
        except CurrencyExchange.DoesNotExist:
            return None
