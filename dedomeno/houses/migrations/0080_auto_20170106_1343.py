# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-06 12:43
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0079_auto_20170104_1727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='good_condition',
        ),
        migrations.AddField(
            model_name='house',
            name='condition',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='date_raw',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='flat_num',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='orientation',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('norte', 'norte'), ('noreste', 'noreste'), ('este', 'este'), ('sureste', 'sureste'), ('sur', 'sur'), ('suroeste', 'suroeste'), ('oeste', 'oeste'), ('noroeste', 'noroeste')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='outside',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
