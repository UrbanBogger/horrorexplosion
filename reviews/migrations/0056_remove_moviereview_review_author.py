# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-11 08:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0055_moviereview_grade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moviereview',
            name='review_author',
        ),
    ]