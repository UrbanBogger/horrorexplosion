# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-10 09:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0067_movie_human_readable_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviereview',
            name='human_readable_url',
            field=models.SlugField(help_text="Enter the 'slug',i.e., the human-readable URL for the movie review", null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='human_readable_url',
            field=models.SlugField(help_text="Enter the 'slug',i.e., the human-readable URL for the movie", null=True, unique=True),
        ),
    ]
