# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-11 22:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0011_auto_20171111_2229'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Reviewer',
        ),
    ]