from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
# Create your models here.


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
        user_obj.active = is_active
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
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
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
    def is_active(self):
        return self.active


class GuestEmail(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
