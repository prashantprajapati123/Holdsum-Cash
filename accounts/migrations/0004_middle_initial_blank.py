# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-06 16:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_not_nullable_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='middle_initial',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
