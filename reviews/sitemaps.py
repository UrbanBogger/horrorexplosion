from django.contrib.sitemaps import Sitemap
from .models import MovieReview, Movie, TelevisionSeries, TelevisionSeason, \
    TelevisionSeasonReview, TelevisionEpisodeReview, MovieFranchise, \
    MovieCreator
from django.core.urlresolvers import reverse


class MovReviewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return MovieReview.objects.all()

    def lastmod(self, item):
        return item.first_created


class MovieSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Movie.objects.all()

    def lastmod(self, item):
         item.first_created


class TVSeriesSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return TelevisionSeries.objects.all()

    def lastmod(self, item):
        item.first_created


class TVSeasonSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return TelevisionSeason.objects.all()

    def lastmod(self, item):
        item.first_created


class TVSeasonRevSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return TelevisionSeasonReview.objects.all()

    def lastmod(self, item):
        item.first_created


class TVEpisodeRevSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return TelevisionEpisodeReview.objects.all()

    def lastmod(self, item):
        item.first_created


class MovFranchiseSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return MovieFranchise.objects.filter(is_publishable=True).all()

    def lastmod(self, item):
        item.last_modified


class MovCreatorSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return MovieCreator.objects.all()


class ListViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return ['movies', 'movie_reviews', 'tv_series', 'mov_franchises',
                'tv-series-review-list']

    def location(self, item):
        return reverse(item)


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
