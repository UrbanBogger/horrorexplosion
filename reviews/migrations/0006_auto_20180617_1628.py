# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-17 15:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20180616_1949'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ['title_for_sorting']},
        ),
        migrations.AlterModelOptions(
            name='moviereview',
            options={'ordering': ['reviewed_movie']},
        ),
        migrations.AddField(
            model_name='movie',
            name='title_for_sorting',
            field=models.CharField(help_text='Enter the title for sorting: Remove all stop words such as "A", "An" and "The" and word all numbers', max_length=250, null=True),
        ),
    ]
