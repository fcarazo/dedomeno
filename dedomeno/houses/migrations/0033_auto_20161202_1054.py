# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 09:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0032_urlsourceterritory_url_source_municipality_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgencySource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agency_source_name', models.CharField(max_length=200)),
                ('agency_source_url', models.CharField(max_length=200)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='houses.Agency')),
            ],
        ),
        migrations.AddField(
            model_name='source',
            name='url_max_request',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='agencysource',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='houses.Source'),
        ),
        migrations.AddField(
            model_name='agency',
            name='agency_source',
            field=models.ManyToManyField(blank=True, through='houses.AgencySource', to='houses.Source'),
        ),
    ]
