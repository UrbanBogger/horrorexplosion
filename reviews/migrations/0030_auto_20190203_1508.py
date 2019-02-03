# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-02-03 15:08
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0029_auto_20190203_1143'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelevisionSeason',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season_title', models.CharField(default='Season', help_text='Enter the title of the television season', max_length=50)),
                ('season_number', models.IntegerField(default=1, help_text='Enter the TV season\'s chronological position in the TV seriesas an integer, e.g. "1" for the first season in the TV series, "2" for the second one, etc.')),
                ('year_of_release', models.IntegerField(blank=True, choices=[(1895, 1895), (1896, 1896), (1897, 1897), (1898, 1898), (1899, 1899), (1900, 1900), (1901, 1901), (1902, 1902), (1903, 1903), (1904, 1904), (1905, 1905), (1906, 1906), (1907, 1907), (1908, 1908), (1909, 1909), (1910, 1910), (1911, 1911), (1912, 1912), (1913, 1913), (1914, 1914), (1915, 1915), (1916, 1916), (1917, 1917), (1918, 1918), (1919, 1919), (1920, 1920), (1921, 1921), (1922, 1922), (1923, 1923), (1924, 1924), (1925, 1925), (1926, 1926), (1927, 1927), (1928, 1928), (1929, 1929), (1930, 1930), (1931, 1931), (1932, 1932), (1933, 1933), (1934, 1934), (1935, 1935), (1936, 1936), (1937, 1937), (1938, 1938), (1939, 1939), (1940, 1940), (1941, 1941), (1942, 1942), (1943, 1943), (1944, 1944), (1945, 1945), (1946, 1946), (1947, 1947), (1948, 1948), (1949, 1949), (1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019)], help_text="Choose the TV serie's release year")),
                ('poster', models.ImageField(help_text='Upload the top-level poster for the TV series', null=True, upload_to='images/')),
                ('poster_thumbnail', models.ImageField(help_text='Upload the top-level poster thumbnail for the TV series', null=True, upload_to='images/')),
                ('duration', models.IntegerField(blank=True, default=90, help_text='Enter the duration of the TV Mini-Series in minutes')),
                ('human_readable_url', models.SlugField(help_text="Enter the 'slug',i.e., the human-readable URL for the TV serie's season", null=True)),
                ('country_of_origin', models.ManyToManyField(help_text='Enter the country of origin', to='reviews.Country')),
                ('genre', models.ManyToManyField(blank=True, help_text="Enter the TV serie's genre(s)", to='reviews.Genre')),
                ('keyword', models.ManyToManyField(blank=True, help_text='Enter the keyword(s) that best describe the TV series picture [OPTIONAL]', to='reviews.Keyword')),
                ('microgenre', models.ManyToManyField(blank=True, help_text="Enter the TV serie's microgenre [OPTIONAL]", to='reviews.Microgenre')),
                ('subgenre', models.ManyToManyField(blank=True, help_text="Enter the TV serie's subgenre [OPTIONAL]", to='reviews.Subgenre')),
            ],
            options={
                'ordering': ['tv_series', 'season_number'],
            },
        ),
        migrations.CreateModel(
            name='TelevisionSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_for_sorting', models.CharField(help_text='Enter the title for sorting: Remove all stop words such as "A", "An" and "The" and word all numbers', max_length=250, null=True)),
                ('poster', models.ImageField(blank=True, help_text='Upload the top-level poster for the TV series if applicable [OPTIONAL]', null=True, upload_to='images/')),
                ('poster_thumbnail', models.ImageField(blank=True, help_text='Upload the top-level poster thumbnail for the TV series if applicable [OPTIONAL]', null=True, upload_to='images/')),
                ('description', ckeditor.fields.RichTextField(blank=True, help_text='Provide background info on the TV series [OPTIONAL]')),
                ('tv_series_type', models.CharField(choices=[('TV Mini-Series', 'TV Mini-Series'), ('Anthology (Episodic) TV Series', 'Anthology (Episodic) TV Series'), ('Serial TV Series', 'Serial TV Series')], max_length=25)),
                ('first_created', models.DateField(auto_now_add=True, null=True)),
                ('human_readable_url', models.SlugField(help_text="Enter the 'slug',i.e., the human-readable URL for the TV series", null=True, unique=True)),
                ('alternative_title', models.ManyToManyField(blank=True, help_text="Enter the TV serie's alternative_title(s) [OPTIONAL]", related_name='tv_series_alternative_title_set', to='reviews.Title')),
                ('main_title', models.ForeignKey(help_text="Enter the TV serie's main title", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tv_series_main_title_set', to='reviews.Title')),
                ('original_title', models.OneToOneField(blank=True, help_text="Enter the TV serie's original title [OPTIONAL]", null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.Title')),
            ],
            options={
                'ordering': ['title_for_sorting'],
            },
        ),
        migrations.AddField(
            model_name='televisionseason',
            name='tv_series',
            field=models.ForeignKey(help_text='Enter the TV series', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tv_series', to='reviews.TelevisionSeries'),
        ),
        migrations.AddField(
            model_name='televisionseason',
            name='tv_series_participation',
            field=models.ManyToManyField(blank=True, help_text='Add the name of the TV series creator, their role and the position you want them to appear in the credits', to='reviews.MovieParticipation'),
        ),
    ]
