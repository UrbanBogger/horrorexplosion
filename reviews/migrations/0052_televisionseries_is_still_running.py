# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-02-16 15:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0051_auto_20190210_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='televisionseries',
            name='is_still_running',
            field=models.NullBooleanField(default=False, help_text='Is TV series still ongoing?'),
        ),
    ]