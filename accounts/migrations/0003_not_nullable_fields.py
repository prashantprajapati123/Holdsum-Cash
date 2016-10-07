# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-05 23:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_fill_out_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='funds_source',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='monthly_income',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='next_paydate',
            field=models.DateField(null=True),
        ),
    ]