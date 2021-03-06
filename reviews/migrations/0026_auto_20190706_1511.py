# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-07-06 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0025_auto_20190701_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='televisionepisode',
            name='imdb_link',
            field=models.CharField(blank=True, help_text='Enter the link to the IMDb', max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='televisionepisodereview',
            name='review_snippet',
            field=models.TextField(blank=True, help_text='Enter the Review snippet for Google Structured Data [OPTIONAL]', max_length=800, null=True),
        ),
        migrations.AddField(
            model_name='televisionseries',
            name='imdb_link',
            field=models.CharField(blank=True, help_text='Enter the link to the IMDb', max_length=250, null=True),
        ),
    ]
