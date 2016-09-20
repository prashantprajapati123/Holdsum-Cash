# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-16 05:47
from __future__ import unicode_literals

from django.db import migrations
import fernet_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_employment'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='plaid_access_token',
            field=fernet_fields.fields.EncryptedCharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='profile',
            name='plaid_public_token',
            field=fernet_fields.fields.EncryptedCharField(blank=True, max_length=200),
        ),
    ]