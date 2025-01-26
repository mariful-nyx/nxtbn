from django.conf import settings
import graphene
from graphql import GraphQLError

from nxtbn.core import CurrencyTypes
from nxtbn.core.admin_types import AdminCurrencyTypesEnum, CurrencyExchangeType
from nxtbn.core.models import CurrencyExchange
from graphene_django.filter import DjangoFilterConnectionField


class AdminCoreQuery(graphene.ObjectType):
    all_currency_exchange = DjangoFilterConnectionField(CurrencyExchangeType)
    currency_exchanges = graphene.Field(CurrencyExchangeType, id=graphene.ID(required=True))
    allowed_currency_list = graphene.List(AdminCurrencyTypesEnum)

    def resolve_all_currency_exchange(self, info, **kwargs):
        return CurrencyExchange.objects.all()
    
    def resolve_currency_exchanges(self, info, id):
        try:
            return CurrencyExchange.objects.get(id=id)
        except CurrencyExchange.DoesNotExist:
            return None
        
    def resolve_allowed_currency_list(self, info):
        allowed_currency_list = settings.ALLOWED_CURRENCIES

        if not allowed_currency_list:
            raise GraphQLError("No allowed currencies found in Server settings.")

        return [
            AdminCurrencyTypesEnum(value=currency[0], label=currency[1])
            for currency in CurrencyTypes.choices
            if currency[0] in allowed_currency_list
        ]
