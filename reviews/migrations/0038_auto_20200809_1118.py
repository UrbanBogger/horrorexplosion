# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2020-08-09 10:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0037_auto_20200803_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributor',
            name='full_name_wo_special_chars',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='alt_title_wo_special_chars',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='main_title_wo_special_chars',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='og_title_wo_special_chars',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='moviecreator',
            name='full_name_wo_special_chars',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='reviewer',
            name='full_name_wo_special_chars',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='televisionepisode',
            name='ep_title_wo_special_chars',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='televisionseason',
            name='season_title_wo_special_chars',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='televisionseries',
            name='alt_title_wo_special_chars',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='televisionseries',
            name='main_title_wo_special_chars',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='televisionseries',
            name='og_title_wo_special_chars',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]