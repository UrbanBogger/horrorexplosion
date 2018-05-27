from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator
from .models import Movie, MovieReview, WebsiteMetadescriptor,\
    sort_titles_with_stop_word, ReferencedMovie

# Create your views here.


def index(request):
    number_of_reviews = MovieReview.objects.all().count()
    number_of_movies = Movie.objects.all().count()
    latest_review = MovieReview.objects.latest('first_created')
    return render(request, 'index.html',
                  context={'number_of_reviews': number_of_reviews,
                           'number_of_movies': number_of_movies,
                           'latest_review': latest_review},)


def about(request):
    mission_statement = WebsiteMetadescriptor.objects.get().mission_statement
    return render(request, 'about.html',
                  context={'mission_statement': mission_statement})


class MovieListView(generic.ListView):
    model = Movie
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(MovieListView, self).get_context_data(**kwargs)
        sorted_movies = sort_titles_with_stop_word(Movie.objects.all(), 'movie')
        paginator = Paginator(sorted_movies, self.paginate_by)
        context['movie_list'] = paginator.page(context['page_obj'].number)
        return context


class MovieDetailView(generic.DetailView):
    model = Movie

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(MovieDetailView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['movie_directors'] = Movie.objects.get(
            pk=self.kwargs.get(
                self.pk_url_kwarg)).return_mov_participation_data('Director')
        context['movie_cast'] = Movie.objects.get(
            pk=self.kwargs.get(
                self.pk_url_kwarg)).return_mov_participation_data('Actor')
        context['associated_reviews'] = Movie.objects.get(
            pk=self.kwargs.get(
                self.pk_url_kwarg)).moviereview_set.all()
        referenced_in_reviews = ReferencedMovie.objects.filter(
            referenced_movie=Movie.objects.get(pk=self.kwargs.get(
                self.pk_url_kwarg)))
        context['referenced_in_reviews'] = referenced_in_reviews
        return context


class MovieReviewListView(generic.ListView):
    model = MovieReview
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(MovieReviewListView, self).get_context_data(**kwargs)
        sorted_mov_reviews = sort_titles_with_stop_word(
            MovieReview.objects.all(), 'review')
        paginator = Paginator(sorted_mov_reviews, self.paginate_by)
        context['moviereview_list'] = paginator.page(
            context['page_obj'].number)
        return context


class MovieReviewDetailView(generic.DetailView):
    model = MovieReview

    def get_context_data(self, **kwargs):
        context = super(MovieReviewDetailView, self).get_context_data(**kwargs)
        context['movie'] = MovieReview.objects.get(pk=self.kwargs.get(
                self.pk_url_kwarg)).reviewed_movie
        context['movie_directors'] = MovieReview.objects.get(
            pk=self.kwargs.get(self.pk_url_kwarg)
             ).reviewed_movie.return_mov_participation_data('Director')
        context['movie_cast'] = MovieReview.objects.get(
            pk=self.kwargs.get(self.pk_url_kwarg)
             ).reviewed_movie.return_mov_participation_data('Actor')
        return context
