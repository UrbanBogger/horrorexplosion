# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-15 14:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0020_movie_is_made_for_tv'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contributor',
            unique_together=set([('first_name', 'middle_name', 'last_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='moviecreator',
            unique_together=set([('first_name', 'middle_name', 'last_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='reviewer',
            unique_together=set([('first_name', 'middle_name', 'last_name')]),
        ),
    ]