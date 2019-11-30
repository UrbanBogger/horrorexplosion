# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-11-30 13:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0028_auto_20191103_1746'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_img_type', models.CharField(choices=[('person', 'person'), ('male', 'male'), ('female', 'female'), ('motion_pic', 'motion_pic')], default=None, help_text='Choose the type of the default image', max_length=12)),
                ('default_img', models.ImageField(default=None, help_text='Upload the default photo', upload_to='generic_images/')),
            ],
        ),
        migrations.AddField(
            model_name='moviecreator',
            name='creator_sex',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female')], default='male', help_text="Choose the movie creator's biological sex", max_length=12),
        ),
    ]
