# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-16 02:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rip_out_yodlee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='employment',
        ),
        migrations.DeleteModel(
            name='Employment',
        ),
    ]
