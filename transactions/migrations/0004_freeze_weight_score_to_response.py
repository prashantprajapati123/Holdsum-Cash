# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-16 02:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_loanrequest_questionresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionresponse',
            name='score',
            field=models.DecimalField(decimal_places=2, default=3, max_digits=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionresponse',
            name='weight',
            field=models.DecimalField(decimal_places=2, default=3, max_digits=4),
            preserve_default=False,
        ),
    ]