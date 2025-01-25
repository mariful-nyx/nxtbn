from django.conf import settings
import graphene

from nxtbn.core import CurrencyTypes
from nxtbn.core.admin_types import CurrencyExchangeType
from nxtbn.core.models import CurrencyExchange

class CurrencyExchangeInput(graphene.InputObjectType):
    id = graphene.ID()
    base_currency = graphene.String(required=True)
    target_currency = graphene.String(required=True)
    exchange_rate = graphene.Decimal(required=True)

class CurrencyExchangeUpdateInput(graphene.InputObjectType):
    exchange_rate = graphene.Decimal(required=True)

class CreateCurrencyExchange(graphene.Mutation):
    class Arguments:
        input = CurrencyExchangeInput(required=True)

    currency_exchange = graphene.Field(CurrencyExchangeType)

    @staticmethod
    def mutate(root, info, input):
        # Validate base_currency
        base_currency = input.base_currency
        if base_currency != settings.BASE_CURRENCY:
            raise Exception("Base currency must match settings.BASE_CURRENCY")

        # Validate target_currency
        allowed_currencies = [choice[0] for choice in CurrencyTypes.choices]
        if input.target_currency not in allowed_currencies:
            raise Exception(f"Target currency '{input.target_currency}' is not allowed.")

        currency_exchange = CurrencyExchange.objects.create(
            base_currency=base_currency,
            target_currency=input.target_currency,
            exchange_rate=input.exchange_rate,
        )
        return CreateCurrencyExchange(currency_exchange=currency_exchange)


class UpdateCurrencyExchange(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        input = CurrencyExchangeUpdateInput(required=True)

    currency_exchange = graphene.Field(CurrencyExchangeType)

    @staticmethod
    def mutate(root, info, id, input):
        try:
            currency_exchange = CurrencyExchange.objects.get(pk=id)
        except CurrencyExchange.DoesNotExist:
            raise Exception("CurrencyExchange not found.")

        currency_exchange.exchange_rate = input.exchange_rate or currency_exchange.exchange_rate
        currency_exchange.save()
        return UpdateCurrencyExchange(currency_exchange=currency_exchange)



class CoreMutation(graphene.ObjectType):
    update_exchange_rate = UpdateCurrencyExchange.Field()
    create_exchange_rate = CreateCurrencyExchange.Field()