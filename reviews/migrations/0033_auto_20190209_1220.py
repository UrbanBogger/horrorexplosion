# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-02-09 12:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0032_auto_20190209_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='televisionseason',
            name='poster_thumbnail',
            field=models.ImageField(blank=True, help_text='Upload the top-level poster thumbnail for the TV series', null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='televisionseries',
            name='poster_thumbnail',
            field=models.ImageField(help_text='Upload the top-level poster thumbnail for the TV series if applicable [OPTIONAL]', null=True, upload_to='images/'),
        ),
    ]