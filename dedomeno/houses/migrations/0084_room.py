# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-08 17:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0083_auto_20170108_1208'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('property_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='houses.Property')),
                ('m2_total', models.IntegerField(blank=True, null=True)),
                ('flat_num', models.CharField(blank=True, max_length=200, null=True)),
                ('elevator', models.NullBooleanField()),
                ('wc', models.IntegerField(blank=True, null=True)),
                ('min_month_stay', models.IntegerField(blank=True, null=True)),
                ('people_max', models.IntegerField(blank=True, null=True)),
                ('people_now_living_gender', models.CharField(blank=True, max_length=200, null=True)),
                ('people_now_living_age_min', models.IntegerField(blank=True, null=True)),
                ('people_now_living_age_max', models.IntegerField(blank=True, null=True)),
                ('smoking_allowed', models.NullBooleanField()),
                ('pet_allowed', models.NullBooleanField()),
                ('looking_for', models.CharField(blank=True, max_length=200, null=True)),
                ('gay_friendly', models.NullBooleanField()),
                ('working', models.NullBooleanField()),
                ('air_conditioner', models.NullBooleanField()),
                ('internet', models.NullBooleanField()),
                ('builtin_wardrobes', models.NullBooleanField()),
                ('furnished', models.NullBooleanField()),
                ('house_cleaners', models.NullBooleanField()),
            ],
            bases=('houses.property',),
        ),
    ]