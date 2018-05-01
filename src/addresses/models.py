from django.db import models
from billing.models import BillingProfile
from django.core.urlresolvers import reverse
# Create your models here.


ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
    ('billing', 'Billing address'),
    ('shipping', 'Shipping address'),
)


class Address(models.Model):

    name = models.CharField(max_length=120, null=True, blank=True, help_text='Shipping to? Who is it for?')
    nickname = models.CharField(max_length=120, null=True, blank=True, help_text='Internal Reference Nickname')
    billing_profile = models.ForeignKey(to=BillingProfile)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line1 = models.CharField(max_length=225)
    address_line2 = models.CharField(max_length=225, blank=True, null=True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    zipcode = models.CharField(max_length=120)
    country = models.CharField(max_length=120)

    def __str__(self):
        if self.nickname:
            return str(self.nickname)
        return str(self.address_line1)

    def get_absolute_url(self):
        return reverse("address-update", kwargs={"pk": self.pk})

    def get_short_address(self):
        for_name = self.name
        if self.nickname:
            for_name = "{} | {},".format(self.nickname, for_name)
        return "{for_name} {line1}, {city}".format(
            for_name=for_name or "",
            line1=self.address_line1,
            city=self.city
        )

    def get_address(self):
        return "{for_name}\n{line1}\n{line2}\n{city}\n{state}, {postal}\n{country}".format(
            for_name=self.name or "",
            line1=self.address_line1,
            line2=self.address_line2 or "",
            city=self.city,
            state=self.state,
            postal=self.zipcode,
            country=self.country
        )