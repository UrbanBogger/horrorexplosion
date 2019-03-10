# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-02-10 09:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0046_televisionseason_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='televisionseries',
            name='tv_series_type',
            field=models.CharField(choices=[('TV Mini-Series', 'Mini-Series'), ('Anthology (Episodic) TV Series', 'Anthology (Episodic)'), ('Serial TV Series', 'Serial')], max_length=25),
        ),
    ]