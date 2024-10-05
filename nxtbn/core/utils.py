import os
from django.conf import settings
from decimal import Decimal, InvalidOperation
from money.money import Currency, Money
from babel.numbers import get_currency_precision, format_currency
from money.exceptions import InvalidAmountError

def make_path(module_path):
    return os.path.join(*module_path.split('.')) + '/'
    


def build_currency_amount(amount: float, currency_code: str, with_symbol: bool = False) -> str:
    """
    Formats and validates a currency amount based on the specified currency code.

    Args:
        amount (float): The amount to be formatted.
        currency_code (str): The currency code (e.g., 'USD').
        with_symbol (bool): Flag to indicate whether to include the currency symbol in the output.

    Returns:
        str: The formatted currency string.

    Raises:
        ValueError: If the amount is invalid for the specified currency.
    """
    # Ensure the currency is valid
    try:
        currency = Currency(currency_code)
    except ValueError:
        raise ValueError(f"Invalid currency code: {currency_code}")

    # Determine the precision for the currency
    try:
        decimal_places = get_currency_precision(currency_code)
    except KeyError:
        raise ValueError(f"Currency precision not found for: {currency_code}")

    # Round the amount to the correct number of decimal places
    try:
        formatted_amount = Decimal(amount).quantize(Decimal(f'1.{"0" * decimal_places}'))
    except (InvalidOperation, ValueError):
        raise ValueError(f"Invalid amount: {amount} for currency '{currency_code}'")

    # Create Money object
    try:
        money = Money(formatted_amount, currency)
    except InvalidAmountError:
        raise ValueError(f"Invalid amount '{formatted_amount}' for currency '{currency_code}'")

    # Format the currency for output
    if with_symbol:
        formatted_currency = format_currency(money.amount, currency_code)
    else:
        formatted_currency = f"{money.amount}"

    return formatted_currency