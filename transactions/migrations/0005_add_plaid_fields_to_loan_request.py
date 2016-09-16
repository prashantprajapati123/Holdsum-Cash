# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-16 06:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_freeze_weight_score_to_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanrequest',
            name='plaid_score',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='loanrequest',
            name='plaid_state',
            field=models.CharField(default='pending', max_length=100),
        ),
    ]
