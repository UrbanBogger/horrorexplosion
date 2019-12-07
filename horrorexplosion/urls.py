"""horrorexplosion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.views.generic import RedirectView, TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from reviews.sitemaps import MovReviewSitemap, MovieSitemap, \
    HomePageSitemap, StaticPagesSitemap, ListViewSitemap, TVSeriesSitemap, \
    TVSeasonSitemap, TVSeasonRevSitemap, TVEpisodeRevSitemap, \
    MovFranchiseSitemap, MovCreatorSitemap

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

urlpatterns += [
    url(r'^reviews/', include('reviews.urls')),
]

sitemaps = {
    'movie_reviews': MovReviewSitemap,
    'movies': MovieSitemap,
    'tv_series': TVSeriesSitemap,
    'tv-season-detail': TVSeasonSitemap,
    'tv-season-review': TVSeasonRevSitemap,
    'tv-episode-review': TVEpisodeRevSitemap,
    'mov-franchise-detail': MovFranchiseSitemap,
    'creator-detail': MovCreatorSitemap,
    'landing_page': HomePageSitemap,
    'static': StaticPagesSitemap,
    'list_views': ListViewSitemap,
}

urlpatterns += [
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

urlpatterns += [
    url(r'^robots.txt', TemplateView.as_view(template_name="robots.txt",
                                             content_type="text/plain")),
]

urlpatterns += [
    url(r'^googled807ca5be9d86494\.html$', lambda r: HttpResponse(
        "google-site-verification: googled807ca5be9d86494.html",
        content_type="text/plain")),
]

urlpatterns += [
    url(r'^BingSiteAuth.xml', TemplateView.as_view(
        template_name="BingSiteAuth.xml", content_type="text/xml")),
]

urlpatterns += [
    url(r'^.*$', RedirectView.as_view(url='/reviews/home/', permanent=True)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

