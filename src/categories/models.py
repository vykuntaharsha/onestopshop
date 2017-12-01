from django.db import models
from django.db.models import Q

# Create your models here.


class CategoryQueryset(models.query.QuerySet):

    def search(self, query):
        lookups = (Q(categoryId__iexact=query) | Q(name__icontains=query) )
        return self.filter(lookups).distinct()


class CategoryManager(models.Manager):

    def get_query_set(self):
        return CategoryQueryset(self.model,self._db)

    def get_by_id(self, _id):
        return self.get_query_set().filter(categoryId__iexact=_id)


class Category(models.Model):
    categoryId = models.CharField(max_length=120, unique=True)
    name = models.CharField(max_length=255)
    subcategories = models.ManyToManyField(to='self', related_name='subcategories')
    category_path = models.ManyToManyField(to='self', related_name='category_path')

    objects = CategoryManager()

    def __str__(self):
        return self.name

