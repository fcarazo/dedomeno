# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-27 23:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0019_auto_20161128_0008'),
    ]

    operations = [
        migrations.AddField(
            model_name='territorialentity',
            name='near_brothers',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='near_brother', to='houses.TerritorialEntity'),
        ),
    ]
