from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url(r'^home/$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contributors/$', views.ContributorListView.as_view(),
        name='contributors'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^thank-you/$', views.thanks, name='thank-you'),
    url(r'^movies/$', views.orderable_movie_list, name='movies'),
    url(r'^movie/(?P<pk>\d+)/(?P<human_readable_url>[-\w]+)$',
        views.MovieDetailView.as_view(), name='movie-detail'),
    url(r'^movie_reviews/$', views.orderable_movreview_list,
        name='movie_reviews'),
    url(r'^movie_review/(?P<pk>\d+)/(?P<human_readable_url>[-\w]+)$',
        views.MovieReviewDetailView.as_view(), name='moviereview-detail'),
    url(r'^creator/(?P<pk>\d+)/(?P<name>[-\w]+)$',
        views.MovieCreatorDetailView.as_view(), name='creator-detail'),
    url(r'^movie-index/', include([
        url(r'^$', views.movie_index, name='movie_index'),
        url(r'^(?P<first_letter>[A-Z]{1})$', views.movie_index,
            name='movie_index_letter'),
            ])
        ),
    url(r'^creator-index/', include([
        url(r'^$', views.creator_index, name='creator-index'),
        url(r'^(?P<first_letter>[A-Z]{1})$', views.creator_index,
            name='creator-index-letter')])),
    url(r'^keyword-index/', include([
        url(r'^$', views.keyword_index, name='keyword_index'),
        url(r'^(?P<first_letter>[A-Z]{1})$', views.keyword_index,
            name='keyword_index_letter')])),
    url(r'^tv-series/', include([
        url(r'^$', views.TVSeriesListView.as_view(),name='tv_series'),
        url(r'^(?P<pk>\d+)/(?P<human_readable_url>[-\w]+)$',
            views.TVSeriesDetailView.as_view(), name='tv-series-detail'),
        url(r'^tv-seasons/(?P<pk>\d+)/(?P<human_readable_url>[-\w]+)$',
            views.TVSeasonDetailView.as_view(), name='tv-season-detail'),
        url(r'^tv-seasons/?', RedirectView.as_view(
                pattern_name='tv_series', permanent=False)),
        url(r'^review-list/$', views.orderable_tvseriesreview_list,
            name='tv-series-review-list'),
        url(r'^tv-reviews/', include([
            url(r'season-reviews/(?P<pk>\d+)/(?P<human_readable_url>['
                r'-\w]+)$', views.TVSeasonReviewDetailView.as_view(),
                name='tv-season-review'),
            url(r'^episode-reviews/(?P<pk>\d+)/(?P<human_readable_url>['
                r'-\w]+)$', views.TVEpisodeReviewDetailView.as_view(),
                name='tv-episode-review'),
            url(r'^$', RedirectView.as_view(
                pattern_name='tv_series', permanent=False)),
            url(r'^season-reviews/?$', RedirectView.as_view(
                pattern_name='tv_series', permanent=False)),
            url(r'^episode-reviews/?$', RedirectView.as_view(
                pattern_name='tv_series', permanent=False)),
            ]),
            ),
    ]),
    ),
    url(r'^film-franchises/$', view=views.MovieFranchiseListView.as_view(),
        name='mov_franchises'),
    url(r'film-franchise-detail/(?P<pk>\d+)/(?P<human_readable_url>[-\w]+)$',
        views.MovieFranchiseDetailView.as_view(), name='mov-franchise-detail'),
    url(r'^keyword/(?P<pk>\d+)/(?P<name>[-\w]+)$',
        views.KeywordDetailView.as_view(), name='keyword-detail')
]
