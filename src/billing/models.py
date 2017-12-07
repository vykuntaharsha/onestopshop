from django.db import models
from django.conf import settings
from accounts.models import GuestEmail
# Create your models here.

User = settings.AUTH_USER_MODEL


class BillingProfileManger(models.Manager):

    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        obj = None
        created = False
        if user.is_authenticated():
            obj, created = self.model.objects.get_or_create(user=user, email=user.email)
        elif guest_email_id is not None:
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(
                email=guest_email_obj.email)
        else:
            pass
        return obj, created


class BillingProfile(models.Model):
    user = models.OneToOneField(to=User, null=True, blank=True)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    objects = BillingProfileManger()

    def __str__(self):
        return self.email
