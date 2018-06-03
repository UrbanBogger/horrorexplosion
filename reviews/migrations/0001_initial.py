# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-03 14:46
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the name of the country', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CreativeRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(help_text='Enter the creative role that a person might have, e.g. Director, Editor, Writer, etc.', max_length=50)),
            ],
            options={
                'ordering': ['role_name'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, default='', max_length=1000)),
                ('name', models.CharField(default='Horror', help_text='Enter the name of the genre', max_length=50)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade_numerical', models.CharField(choices=[('0.5', '0.5'), ('1.0', '1.0'), ('1.5', '1.5'), ('2.0', '2.0'), ('2.5', '2.5'), ('3.0', '3.0'), ('3.5', '3.5'), ('4.0', '4.0')], default=('2.5', '2.5'), help_text="Choose the motion picture's grade", max_length=3)),
                ('grade_description', models.CharField(help_text='Enter a short description of the grade', max_length=50)),
                ('grade_depiction', models.ImageField(help_text='Upload the image corresponding to the grade', null=True, upload_to='grade_depictions/')),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, default='', max_length=1000)),
                ('name', models.CharField(help_text='Enter the keyword (or a keyword phrase)', max_length=100)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Microgenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, default='', max_length=1000)),
                ('name', models.CharField(help_text='Enter the name of the microgenre', max_length=50)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_of_release', models.IntegerField(choices=[(1895, 1895), (1896, 1896), (1897, 1897), (1898, 1898), (1899, 1899), (1900, 1900), (1901, 1901), (1902, 1902), (1903, 1903), (1904, 1904), (1905, 1905), (1906, 1906), (1907, 1907), (1908, 1908), (1909, 1909), (1910, 1910), (1911, 1911), (1912, 1912), (1913, 1913), (1914, 1914), (1915, 1915), (1916, 1916), (1917, 1917), (1918, 1918), (1919, 1919), (1920, 1920), (1921, 1921), (1922, 1922), (1923, 1923), (1924, 1924), (1925, 1925), (1926, 1926), (1927, 1927), (1928, 1928), (1929, 1929), (1930, 1930), (1931, 1931), (1932, 1932), (1933, 1933), (1934, 1934), (1935, 1935), (1936, 1936), (1937, 1937), (1938, 1938), (1939, 1939), (1940, 1940), (1941, 1941), (1942, 1942), (1943, 1943), (1944, 1944), (1945, 1945), (1946, 1946), (1947, 1947), (1948, 1948), (1949, 1949), (1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018)], help_text="Choose the motion picture's release year")),
                ('duration', models.IntegerField(default=90, help_text='Enter the duration of the motion picture in minutes')),
                ('poster', models.ImageField(blank=True, help_text='Upload the poster of the movie', null=True, upload_to='movie_posters/')),
                ('is_direct_to_video', models.NullBooleanField(default=False, help_text='Is the movie direct-to-video/DVD?')),
                ('is_made_for_tv', models.NullBooleanField(default=False, help_text='Is the movie made-for-TV?')),
                ('is_a_sequel', models.NullBooleanField(default=False, help_text='Is this movie a sequel?')),
                ('is_a_remake', models.NullBooleanField(default=False, help_text='Is this movie a remake?')),
            ],
            options={
                'ordering': ['main_title'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MovieCreator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('biography', models.TextField(blank=True, max_length=1000)),
            ],
            options={
                'ordering': ['last_name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MovieFranchise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('franchise_name', models.CharField(help_text='Enter the name of the movie franchise', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MovieParticipation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creative_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.CreativeRole')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.MovieCreator')),
            ],
            options={
                'ordering': ['person'],
            },
        ),
        migrations.CreateModel(
            name='MovieReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', ckeditor.fields.RichTextField(help_text='Enter the review text')),
                ('date_created', models.DateField(help_text='Enter the original date of the review creation')),
                ('last_modified', models.DateField(auto_now=True)),
                ('first_created', models.DateField(auto_now_add=True, null=True)),
                ('mov_review_page_description', models.CharField(default='Click on the link to see what we have to say about this flick.', max_length=155)),
                ('grade', models.ForeignKey(help_text="Choose the motion picture's grade", null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.Grade')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReferencedMovie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referenced_movie', models.ManyToManyField(help_text='Add the referenced movie(s)', to='reviews.Movie')),
                ('review', models.ForeignKey(help_text='Add the review where the movie was referenced', null=True, on_delete=django.db.models.deletion.CASCADE, to='reviews.MovieReview')),
            ],
        ),
        migrations.CreateModel(
            name='Reviewer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('biography', models.TextField(blank=True, max_length=1000)),
            ],
            options={
                'ordering': ['last_name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subgenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, default='', max_length=1000)),
                ('name', models.CharField(help_text='Enter the name of the subgenre', max_length=50)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='WebsiteMetadescriptor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website_name', models.CharField(max_length=50)),
                ('contact_info', models.EmailField(help_text='Enter a contact email', max_length=50)),
                ('mission_statement', ckeditor.fields.RichTextField(blank=True)),
                ('landing_page_title', models.CharField(default='The Horror Explosion', max_length=50)),
                ('landing_page_description', models.CharField(default='Reviewing and analyzing post-1999 horror movies.', max_length=155)),
            ],
        ),
        migrations.AddField(
            model_name='moviereview',
            name='review_author',
            field=models.ForeignKey(help_text='Enter the author of the review', null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.Reviewer'),
        ),
        migrations.AddField(
            model_name='moviereview',
            name='reviewed_movie',
            field=models.ForeignKey(help_text='Specify the reviewed movie', null=True, on_delete=django.db.models.deletion.CASCADE, to='reviews.Movie'),
        ),
        migrations.AddField(
            model_name='movie',
            name='alternative_title',
            field=models.ManyToManyField(blank=True, help_text="Enter the motion picture's alternative_title(s) [OPTIONAL]", related_name='alternative_titles', to='reviews.Title'),
        ),
        migrations.AddField(
            model_name='movie',
            name='country_of_origin',
            field=models.ManyToManyField(help_text='Enter the country of origin', to='reviews.Country'),
        ),
        migrations.AddField(
            model_name='movie',
            name='franchise_association',
            field=models.ManyToManyField(blank=True, help_text='If applicable, choose the franchise that the movie belongs to', to='reviews.MovieFranchise'),
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(help_text="Enter the motion picture's genre(s)", to='reviews.Genre'),
        ),
        migrations.AddField(
            model_name='movie',
            name='keyword',
            field=models.ManyToManyField(help_text='Enter the keyword(s) that best describe the motion picture', to='reviews.Keyword'),
        ),
        migrations.AddField(
            model_name='movie',
            name='main_title',
            field=models.ForeignKey(help_text="Enter the motion picture's main title", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.Title'),
        ),
        migrations.AddField(
            model_name='movie',
            name='microgenre',
            field=models.ManyToManyField(blank=True, help_text="Enter the motion picture's microgenre [OPTIONAL]", to='reviews.Microgenre'),
        ),
        migrations.AddField(
            model_name='movie',
            name='movie_participation',
            field=models.ManyToManyField(help_text='Add the name of the movie creator and their role', to='reviews.MovieParticipation'),
        ),
        migrations.AddField(
            model_name='movie',
            name='original_title',
            field=models.OneToOneField(blank=True, help_text="Enter the motion picture's original title [OPTIONAL]", null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.Title'),
        ),
        migrations.AddField(
            model_name='movie',
            name='subgenre',
            field=models.ManyToManyField(blank=True, help_text="Enter the motion picture's subgenre [OPTIONAL]", to='reviews.Subgenre'),
        ),
    ]
