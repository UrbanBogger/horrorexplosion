# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-02 18:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0061_moviereview_mov_review_page_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviereview',
            name='mov_review_page_description',
            field=models.CharField(default='', max_length=155),
        ),
    ]