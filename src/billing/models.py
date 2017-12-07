from django.db import models
from django.conf import settings
# Create your models here.

User = settings.AUTH_USER_MODEL


class BillingProfile(models.Model):
    user = models.OneToOneField(to=User, null=True, blank=True)
    email = models.EmailField()
    billing_address = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
