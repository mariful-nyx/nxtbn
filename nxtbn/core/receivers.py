from django.db.models.signals import post_migrate
from django.dispatch import receiver
from nxtbn.core.models import InvoiceSettings, SiteSettings
from django.contrib.sites.models import Site


@receiver(post_migrate)
def create_default_site_settings(sender, **kwargs):
    if SiteSettings.objects.count() == 0:
        site, created = Site.objects.get_or_create(
            domain="example.com", defaults={"name": "Default Site"}
        )
        
        SiteSettings.objects.create(
            site=site,
            site_name="nxtbn commerce",
            company_name="Default Company Name",
            contact_email="contact@example.com",
            contact_phone="123456789",
            address="Default Address",
        )
        print("SiteSettings instance created.")

    if InvoiceSettings.objects.count() == 0:
        site, created = Site.objects.get_or_create(
            domain="example.com", defaults={"name": "Default Site"}
        )
        
        InvoiceSettings.objects.create(
            site=site,
            store_name="nxtbn commerce",
            store_address="Default Store Address",
            city="Default City",
            country="Default Country",
            postal_code="123456",
            contact_email="invoice@example.com",
        )