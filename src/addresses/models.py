from django.db import models
from billing.models import BillingProfile
# Create your models here.


ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping')
)


class Address(models.Model):
    billing_profile = models.ForeignKey(to=BillingProfile)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line1 = models.CharField(max_length=225)
    address_line2 = models.CharField(max_length=225, blank=True, null=True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    zipcode = models.CharField(max_length=120)
    country = models.CharField(max_length=120)

    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        return f'{self.address_line1}, {self.address_line2} {self.city}, {self.state}, {self.zipcode}'
