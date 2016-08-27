# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-27 22:17
from __future__ import unicode_literals

from django.db import migrations
import fernet_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_use_localflavor_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='yodleepw',
            field=fernet_fields.fields.EncryptedCharField(default='', max_length=140),
            preserve_default=False,
        ),
    ]
