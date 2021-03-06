# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-05 22:02
from __future__ import unicode_literals

import accounts.fields
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='funds_source',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='middle_initial',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='monthly_income',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='next_paydate',
            field=models.DateField(default=datetime.date(2016, 10, 5)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='pay_frequency',
            field=models.CharField(choices=[('monthly', 'Monthly'), ('biweekly', 'Bi-Weekly'), ('bimonthly', 'Bi-Monthly')], default='monthly', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='ssn',
            field=accounts.fields.EncryptedSSNField(default=''),
            preserve_default=False,
        ),
    ]
