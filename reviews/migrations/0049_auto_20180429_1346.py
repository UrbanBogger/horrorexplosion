# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-29 12:46
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0048_auto_20180429_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviereview',
            name='review_text',
            field=ckeditor.fields.RichTextField(help_text='Enter the review text'),
        ),
    ]