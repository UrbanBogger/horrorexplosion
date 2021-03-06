# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-23 19:09
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20180617_1907'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', ckeditor.fields.RichTextField(help_text='Enter the text', verbose_name='Text')),
                ('date_created', models.DateField(help_text='Enter the original date of the text creation')),
                ('last_modified', models.DateField(auto_now=True)),
                ('first_created', models.DateField(auto_now_add=True, null=True)),
                ('review_author', models.ForeignKey(help_text='Enter the name of the author', null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.Reviewer', verbose_name='Text Author')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='moviereview',
            name='date_created',
            field=models.DateField(help_text='Enter the original date of the text creation'),
        ),
        migrations.AlterField(
            model_name='moviereview',
            name='review_author',
            field=models.ForeignKey(help_text='Enter the name of the author', null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.Reviewer', verbose_name='Text Author'),
        ),
        migrations.AlterField(
            model_name='moviereview',
            name='review_text',
            field=ckeditor.fields.RichTextField(help_text='Enter the text', verbose_name='Text'),
        ),
    ]
