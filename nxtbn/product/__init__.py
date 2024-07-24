from django.db import models

class WeightUnits(models.TextChoices):
    """Defines standard units of weight for product measurement.

    - 'GRAM': Weight in grams.
    - 'KILOGRAM': Weight in kilograms.
    - 'POUND': Weight in pounds.
    - 'OUNCE': Weight in ounces.
    - 'TON': Weight in tons.
    """

    GRAM = 'GRAM', 'Gram'
    KILOGRAM = 'KG', 'Kilogram'
    POUND = 'LB', 'Pound'
    OUNCE = 'OZ', 'Ounce'
    TON = 'TON', 'Ton'



class StockStatus(models.TextChoices):
    """Defines the stock availability status for products.

    - 'IN_STOCK': The product is available and in stock.
    - 'OUT_OF_STOCK': The product is currently out of stock.
    """

    IN_STOCK = 'IN_STOCK', 'In Stock'
    OUT_OF_STOCK = 'OUT_OF_STOCK', 'Out of Stock'
