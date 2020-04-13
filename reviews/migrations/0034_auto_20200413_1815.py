# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2020-04-13 17:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0033_auto_20200131_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributor',
            name='photo_thumb',
            field=models.ImageField(blank=True, default=None, help_text="Upload the thumb of the person's photo", null=True, upload_to='people/'),
        ),
        migrations.AddField(
            model_name='defaultimage',
            name='default_img_thumb',
            field=models.ImageField(blank=True, default=None, help_text='Upload the thumb of the default photo', null=True, upload_to='generic_images/'),
        ),
        migrations.AddField(
            model_name='moviecreator',
            name='photo_thumb',
            field=models.ImageField(blank=True, default=None, help_text="Upload the thumb of the person's photo", null=True, upload_to='people/'),
        ),
        migrations.AddField(
            model_name='reviewer',
            name='photo_thumb',
            field=models.ImageField(blank=True, default=None, help_text="Upload the thumb of the person's photo", null=True, upload_to='people/'),
        ),
        migrations.AlterField(
            model_name='defaultimage',
            name='default_img_type',
            field=models.CharField(choices=[('person', 'person'), ('male', 'male'), ('female', 'female'), ('motion_pic', 'motion_pic'), ('keyword', 'keyword')], default=None, help_text='Choose the type of the default image', max_length=12),
        ),
    ]