# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-03 17:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0068_auto_20170103_1753'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='address',
            new_name='address_raw',
        ),
    ]
