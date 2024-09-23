from django.db import models
from nxtbn.core import CurrencyTypes
from nxtbn.core.models import AbstractBaseModel
from django_countries.fields import CountryField

class ShippingMethod(AbstractBaseModel):
    """
    Represents different shipping methods offered by a carrier, such as Standard or Express Shipping.

    Fields:
        - name: The name of the shipping method (e.g., "Express Shipping").
        - description: An optional text field to provide a detailed description of the method.
        - carrier: The name of the shipping carrier offering the method (e.g., "FedEx", "DHL").
    
    Examples:
        - FedEx - Standard Shipping
        - DHL - Express Shipping
    """
    name = models.CharField(max_length=200, help_text="The name of the shipping method, e.g., 'Standard Shipping'.")
    description = models.TextField(blank=True, null=True, help_text="Optional detailed description of the shipping method.")
    carrier = models.CharField(max_length=200, help_text="Shipping carrier, e.g., 'FedEx', 'DHL'.")

    def __str__(self):
        """
        Returns a human-readable representation of the ShippingMethod instance.
        Example: "FedEx - Express Shipping"
        """
        return f"{self.carrier} - {self.name}"


class ShippingRate(AbstractBaseModel):
    """
    Stores the shipping cost for a specific method, based on weight, country, and region.
    Each ShippingMethod can have multiple rates depending on these factors.
    
    Fields:
        - shipping_method: A foreign key linking the rate to a specific ShippingMethod.
        - country: Optional field specifying the country this rate applies to. Blank means global rates.
        - region: Optional field for specifying a region within a country (e.g., "California").
        - city: Optional field for more localized rates within a city (e.g., "San Francisco").
        - weight_min: Minimum weight (in kilograms) for the rate to be applicable.
        - weight_max: Maximum weight (in kilograms) for the rate to be applicable.
        - rate: The shipping cost for packages that meet the weight and location criteria.
        - currency: The currency in which the rate is expressed (linked to the Currency model).

    Examples:
        - DHL Express Shipping for packages between 0kg and 5kg in the US costs $25.00.
        - FedEx Standard Shipping for packages between 5kg and 10kg globally costs $30.00.
    """
    shipping_method = models.ForeignKey(
        ShippingMethod, on_delete=models.CASCADE, related_name="rates",
        help_text="The shipping method this rate applies to."
    )
    country = CountryField(blank=True, null=True, help_text="If blank, the rate applies globally.")
    region = models.CharField(max_length=200, blank=True, null=True, help_text="Region within the country, e.g., 'California'. If blank, applies nationwide.")
    city = models.CharField(max_length=200, blank=True, null=True, help_text="Specific city within the region, e.g., 'San Francisco'.")
    weight_min = models.DecimalField(max_digits=10, decimal_places=2, help_text="Minimum weight (in kg) for this rate.")
    weight_max = models.DecimalField(max_digits=10, decimal_places=2, help_text="Maximum weight (in kg) for this rate.")
    rate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Shipping cost for this rate.")
    currency = models.CharField(
        max_length=3,
        default=CurrencyTypes.USD,
        choices=CurrencyTypes.choices,
    )

    def __str__(self):
        """
        Returns a human-readable representation of the ShippingRate instance.
        Example: "FedEx - Standard Shipping - US (California, San Francisco) (0kg to 5kg)"
        """
        location = ", ".join(filter(None, [self.city, self.region, self.country.name if self.country else "Global"]))
        return f"{self.shipping_method} - {location} ({self.weight_min}kg to {self.weight_max}kg)"
