# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-04 10:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='shipping',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100),
        ),
    ]
