# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-27 11:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0058_auto_20180527_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='is_a_remake',
            field=models.NullBooleanField(default=False, help_text='Is this movie a remake?'),
        ),
    ]
