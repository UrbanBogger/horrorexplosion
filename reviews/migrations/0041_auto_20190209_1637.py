# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-02-09 16:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0040_televisionreview_human_readable_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='televisionreview',
            options={'ordering': ['reviewed_tv_season', 'reviewed_tv_episode']},
        ),
    ]