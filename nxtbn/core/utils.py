import os
from django.conf import settings
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
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
        currency_code (str): The currency code (e.g., 'USD', 'KWD', 'OMR', 'JPY').
        with_symbol (bool): Flag to indicate whether to include the currency symbol in the output.

    Returns:
        str: The formatted currency string.

    Raises:
        ValueError: If the amount is invalid for the specified currency.

    # Example usage:
    print(build_currency_amount(204.170, 'USD'))  # Output: "$ 204.17"
    print(build_currency_amount(204.170, 'KWD'))  # Output: "د.ك 204.170"
    print(build_currency_amount(204.000, 'JPY'))      # Output: "¥ 204"  # JPY has 0 decimal places
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
        formatted_amount = Decimal(amount).quantize(Decimal(f'1.{"0" * decimal_places}'), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        raise ValueError(f"Invalid amount: {amount} for currency '{currency_code}'")

    # Create Money object (optional)
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


def to_currency_subunit(amount: float, currency_code: str) -> int:
    """
    Converts a given amount to subunits (like cents for USD or fils for KWD) based on the currency.

    Args:
        amount (float): The amount to be converted to subunits.
        currency_code (str): The currency code (e.g., 'USD', 'KWD').

    Returns:
        int: The amount in subunits.

    # Example usage:
    print(to_currency_subunit(204.170, 'USD'))  # Output: 20417 (in cents)
    print(to_currency_subunit(204.170, 'KWD'))  # Output: 204170 (in fils)
    print(to_currency_subunit(204.000, 'JPY'))  # Output: 204 (no subunits for JPY)
    """
    # Ensure the currency is valid
    try:
        currency = Currency(currency_code)
    except ValueError:
        raise ValueError(f"Invalid currency code: {currency_code}")

    # Get the correct number of decimal places for the currency (subunit factor)
    try:
        decimal_places = get_currency_precision(currency_code)
    except KeyError:
        raise ValueError(f"Currency precision not found for: {currency_code}")

    # Multiply the amount by 10^decimal_places to convert it into subunits (e.g., 20.45 USD -> 2045 cents)
    try:
        subunit_amount = Decimal(amount) * (10 ** decimal_places)
        subunit_amount = subunit_amount.quantize(Decimal('1'), rounding=ROUND_HALF_UP)  # Round to the nearest whole number
    except (InvalidOperation, ValueError):
        raise ValueError(f"Invalid amount: {amount} for currency '{currency_code}'")

    return int(subunit_amount)