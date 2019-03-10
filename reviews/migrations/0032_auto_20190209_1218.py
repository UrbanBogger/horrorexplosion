# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-02-09 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0031_auto_20190203_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='televisionseason',
            name='poster',
            field=models.ImageField(blank=True, help_text='Upload the top-level poster for the TV series', null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='televisionseries',
            name='poster',
            field=models.ImageField(help_text='Upload the top-level poster for the TV series if applicable [OPTIONAL]', null=True, upload_to='images/'),
        ),
    ]