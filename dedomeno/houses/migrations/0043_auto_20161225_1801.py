# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-25 17:01
from __future__ import unicode_literals

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0042_auto_20161223_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='orientation',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('N', 'N'), ('NE', 'NE'), ('E', 'E'), ('SE', 'SE'), ('S', 'S'), ('SW', 'SW'), ('W', 'W'), ('NW', 'NW')], max_length=2, null=True),
        ),
    ]