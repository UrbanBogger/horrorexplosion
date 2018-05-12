# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-15 15:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0036_auto_20180415_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferencedMovie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='movie',
            name='review',
        ),
        migrations.AddField(
            model_name='referencedmovie',
            name='referenced_movie',
            field=models.ForeignKey(help_text='Add the referenced movie', null=True, on_delete=django.db.models.deletion.CASCADE, to='reviews.Movie'),
        ),
        migrations.AddField(
            model_name='referencedmovie',
            name='review',
            field=models.ForeignKey(help_text='Add the review where the movie was referenced', null=True, on_delete=django.db.models.deletion.CASCADE, to='reviews.Review'),
        ),
    ]
