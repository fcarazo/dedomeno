# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-18 10:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0099_auto_20170117_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='real_estate',
            field=models.ForeignKey(blank=True, help_text='If blank there is not a real estate involved', null=True, on_delete=django.db.models.deletion.SET_NULL, to='houses.RealEstate'),
        ),
    ]
