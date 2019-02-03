# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-08-26 17:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20180826_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='movieremake',
            name='remake',
            field=models.ManyToManyField(help_text='Add the remake(s) of this movie', related_name='remake', to='reviews.Movie'),
        ),
    ]