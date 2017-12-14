import os
import random
import sys
from urllib import parse

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.urls import reverse

from categories.models import Category
from mainwebsite.utils import unique_slug_generator


# Create your models here.


def get_filename_ext(file_path):
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, file_name):
    new_filename = random.randint(1, sys.maxsize)
    name, ext = get_filename_ext(file_name)
    final_file_name = f'{new_filename}{ext}'
    return f'products/{new_filename}/{final_file_name}'


class ProductQueryset(models.query.QuerySet):

    def search(self, query):
        lookups = (Q(name__icontains=query) |
                   Q(categories__name__icontains=query)|
                   Q(description__icontains=query) |
                   Q(price__icontains=query))
        # tshirt, t-shirt, t shirt, red, green, blue,
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQueryset(self.model, self._db)

    def get_by_id(self, _id):
        return self.get_queryset().filter(id=_id)

    def search(self, query):
        return self.get_queryset().search(query=query)


class Product(models.Model):
    product_id = models.CharField(unique=True, max_length=225)
    name = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    upc = models.CharField(max_length=255, null=True)
    shipping = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    description = models.TextField(null=True)
    manufacturer = models.CharField(max_length=255, null=True)
    model = models.CharField(max_length=255, null=True)
    image = models.ImageField(max_length=255, upload_to=upload_image_path, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)
    slug = models.SlugField(max_length=500, null=True, blank=True, unique=True)
    categories = models.ManyToManyField(to=Category)

    objects = ProductManager()

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        return str(self.image)

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={'slug': self.slug})

    def get_categories(self):
        return self.categories.all()


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)

