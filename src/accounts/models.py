from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
# Create your models here.
from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings
from mainwebsite.utils import unique_key_generator
from django.db.models.signals import post_save, pre_save
from datetime import timedelta
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db.models import Q


DEFAULT_ACTIVATION_DAYS = getattr(settings, 'DEFAULT_ACTIVATION_DAYS', 7)


class UserManager(BaseUserManager):
    def create_user(self, full_name, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Users should have an email address')
        if not password:
            raise ValueError('Users must have a password')
        if not full_name:
            raise ValueError('Users must have a full name')

        user_obj = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        user_obj.set_password(password)
        user_obj.is_active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using=self.db)
        return user_obj

    def create_staffuser(self, full_name, email, password=None):
        user = self.create_user(full_name=full_name, email=email, password=password, is_staff=True)
        return user

    def create_superuser(self,full_name, email, password=None):
        user = self.create_user(full_name=full_name, email=email, password=password, is_admin=True, is_staff=True)
        return user


class User(AbstractBaseUser):

    email = models.EmailField(unique=True, max_length=255)
    full_name = models.CharField(max_length=225)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def active(self):
        return self.is_active


class EmailActivationQueryset(models.query.QuerySet):

    def confirmable(self):
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        end_range = now
        return self.filter(activated=False, forced_expired=False).filter(
            timestamp__gt=start_range, timestamp__lte=end_range)


class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQueryset(self.model, using=self.db)

    def confirmable(self):
        return self.get_queryset().confirmable()

    def email_exists(self, email):
        return self.get_queryset().filter( Q(email=email) | Q(user__email=email)).filter(activated=False)

class EmailActivation(models.Model):
    user = models.ForeignKey(to=User)
    email = models.EmailField()
    key = models.CharField(max_length=120, blank=True, null=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    expires = models.IntegerField(default=7)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.user.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable()
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            user = self.user
            user.is_active = True
            user.save()
            self.activated = True
            self.save()
            return True
        return False

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url = getattr(settings, 'BASE_URL', 'https://onestop-shop.herokuapp.com')
                key_path = reverse("account:email-activate", kwargs={'key': self.key})
                path = f'{base_url}{key_path}'
                context = {
                    'path': path,
                    'email': self.email
                }
                txt_ = get_template('registration/emails/verify.txt').render(context)
                html_ = get_template('registration/emails/verify.html').render(context)
                subject = '1 click email verification'
                sent_mail = send_mail(
                    subject=subject,
                    message=txt_,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    html_message=html_,
                    recipient_list=[self.email],
                    fail_silently=False
                )
                return sent_mail
        return False


def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)


pre_save.connect(pre_save_email_activation, sender=EmailActivation)


def post_save_user_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        obj.send_activation()


post_save.connect(post_save_user_create_receiver, sender=User)


class GuestEmail(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
