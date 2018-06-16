# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-11 08:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0056_remove_moviereview_review_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviereview',
            name='review_author',
            field=models.ForeignKey(help_text='Enter the author of the review', null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.Reviewer'),
        ),
    ]