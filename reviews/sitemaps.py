from django.contrib.sitemaps import Sitemap
from .models import MovieReview, Movie
from django.core.urlresolvers import reverse


class MovReviewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return MovieReview.objects.all()

    def lastmod(self, item):
        return item.first_created


class MovieSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Movie.objects.all()

    def lastmod(self, item):
         item.first_created


class HomePageSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return ['index']

    def location(self, item):
        return reverse(item)


class StaticPagesSitemap(Sitemap):
    changefreq = 'yearly'
    priority = 0.5

    def items(self):
        return ['about', 'contributors', 'contact']

    def location(self, item):
        return reverse(item)
