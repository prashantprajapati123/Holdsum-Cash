# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-12 01:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import fernet_fields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employer', models.CharField(default=b'', max_length=100)),
                ('role', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('zipCode', models.CharField(max_length=20)),
                ('monthly_income', fernet_fields.fields.EncryptedIntegerField(default=0)),
                ('income_frequency', models.DurationField()),
                ('next_pay_date', fernet_fields.fields.EncryptedDateField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DOB', fernet_fields.fields.EncryptedDateField()),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('zipCode', models.CharField(max_length=20)),
                ('SSN', fernet_fields.fields.EncryptedCharField(max_length=15)),
                ('status', models.CharField(choices=[(b'pending', b'Pending Approval'), (b'approved', b'Approved'), (b'denied', b'Denied')], default=b'pending', max_length=20)),
                ('employed', models.CharField(choices=[(b'unemp', b'Unemployed'), (b'selfemp', b'Self Employed'), (b'ft', b'Full Time'), (b'pt', b'Part Time'), (b'stu', b'Student')], default=b'unemp', max_length=30)),
                ('employment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.Employment')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
