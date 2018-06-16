# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-10 12:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0054_remove_moviereview_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviereview',
            name='grade',
            field=models.ForeignKey(help_text="Choose the motion picture's grade", null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.Grade'),
        ),
    ]