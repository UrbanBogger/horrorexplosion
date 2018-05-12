# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-11 22:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20171111_2038'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='websitemetadescriptors',
            name='contact_info',
            field=models.EmailField(help_text='Enter a contact email', max_length=50),
        ),
    ]
