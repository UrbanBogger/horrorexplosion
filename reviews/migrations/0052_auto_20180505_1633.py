# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-05 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0051_auto_20180505_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade_numerical', models.CharField(choices=[('0.5', '0.5'), ('1.0', '1.0'), ('1.5', '1.5'), ('2.0', '2.0'), ('2.5', '2.5'), ('3.0', '3.0'), ('3.5', '3.5'), ('4.0', '4.0')], default=('2.5', '2.5'), help_text="Choose the motion picture's grade", max_length=3)),
                ('grade_description', models.CharField(help_text='Enter a short description of the grade', max_length=50)),
                ('grade_depiction', models.ImageField(help_text='Upload the image corresponding to the grade', null=True, upload_to='images/')),
            ],
        ),
        migrations.RemoveField(
            model_name='moviereview',
            name='grade',
        ),
        migrations.AddField(
            model_name='moviereview',
            name='grade',
            field=models.ManyToManyField(help_text="Choose the motion picture's grade", to='reviews.Grade'),
        ),
    ]
