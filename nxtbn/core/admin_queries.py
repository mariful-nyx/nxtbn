from django.conf import settings
import graphene
from graphql import GraphQLError

from nxtbn.core import CurrencyTypes
from nxtbn.core.admin_permissions import check_user_permissions
from nxtbn.core.admin_types import AdminCurrencyTypesEnum, CurrencyExchangeType
from nxtbn.core.models import CurrencyExchange
from graphene_django.filter import DjangoFilterConnectionField


class AdminCoreQuery(graphene.ObjectType):
    currency_exchanges = DjangoFilterConnectionField(CurrencyExchangeType)
    currency_exchange = graphene.Field(CurrencyExchangeType, id=graphene.ID(required=True))
    allowed_currency_list = graphene.List(AdminCurrencyTypesEnum)

    def resolve_currency_exchanges(self, info, **kwargs):
        check_user_permissions(info, any_staff=True)
        return CurrencyExchange.objects.all()
    
    def resolve_currency_exchange(self, info, id):
        check_user_permissions(info, any_staff=True)
        try:
            return CurrencyExchange.objects.get(id=id)
        except CurrencyExchange.DoesNotExist:
            return None
        
    def resolve_allowed_currency_list(self, info):
        check_user_permissions(info, any_staff=True)
        allowed_currency_list = settings.ALLOWED_CURRENCIES

        if not allowed_currency_list:
            raise GraphQLError("No allowed currencies found in Server settings.")

        return [
            AdminCurrencyTypesEnum(value=currency[0], label=currency[1])
            for currency in CurrencyTypes.choices
            if currency[0] in allowed_currency_list
        ]
