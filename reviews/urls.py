from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contributors/$', views.ContributorListView.as_view(),
        name='contributors'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^movies/$', views.MovieListView.as_view(), name='movies'),
    url(r'^movie/(?P<pk>\d+)$', views.MovieDetailView.as_view(),
        name='movie-detail'),
    url(r'movie/(?P<pk>\d+)/(?P<human_readable_url>[-\w]+)$',
        views.MovieDetailView.as_view(),
        name='movie-detail'),
    url(r'^movie_reviews/$', views.MovieReviewListView.as_view(),
        name='movie_reviews'),
    url(r'^movie_review/(?P<pk>\d+)/(?P<human_readable_url>[-\w]+)$',
        views.MovieReviewDetailView.as_view(), name='moviereview-detail'),
]
