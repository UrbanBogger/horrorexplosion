from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator
from .models import Movie, MovieReview, WebsiteMetadescriptor,\
    sort_titles_with_stop_word, ReferencedMovie, Contributor

# Create your views here.


def index(request):
    number_of_reviews = MovieReview.objects.all().count()
    number_of_movies = Movie.objects.all().count()
    latest_review = MovieReview.objects.latest('first_created')
    home_page_title = WebsiteMetadescriptor.objects.get().landing_page_title
    content_metadescription = WebsiteMetadescriptor.\
        objects.get().landing_page_description
    return render(request, 'index.html',
                  context={'page_title': home_page_title,
                           'meta_content_description': content_metadescription,
                           'number_of_reviews': number_of_reviews,
                           'number_of_movies': number_of_movies,
                           'latest_review': latest_review},)


def about(request):
    mission_statement = WebsiteMetadescriptor.objects.get().mission_statement
    about_page_title = "About The Horror Explosion Website"
    content_metadescription = "What The Horror Explosion website is all about."
    return render(request, 'about.html',
                  context={'page_title': about_page_title,
                           'meta_content_description': content_metadescription,
                           'mission_statement': mission_statement})


def contact(request):
    contact_page_title = "Contact Info | The Horror Explosion"
    content_metadescription = "The Horror Explosion website contact info"
    return render(request, 'contact.html',
                  context={'page_title': contact_page_title,
                           'meta_content_description': content_metadescription}
                  )


class ContributorListView (generic.ListView):
    model = Contributor
    contributors_page_title = "Contributors | The Horror Explosion"
    content_metadescription = "The list of people who contribute content to " \
                              "our website"

    def get_context_data(self, **kwargs):
        context = super(ContributorListView, self).get_context_data(**kwargs)
        context['page_title'] = self.contributors_page_title
        context['meta_content_description'] = self.content_metadescription
        return context


class MovieListView(generic.ListView):
    model = Movie
    paginate_by = 5
    movie_list_page_title = "Movie List | The Horror Explosion"
    content_metadescription = "The list of all the movies in our database."

    def get_context_data(self, **kwargs):
        context = super(MovieListView, self).get_context_data(**kwargs)
        sorted_movies = sort_titles_with_stop_word(Movie.objects.all(), 'movie')
        paginator = Paginator(sorted_movies, self.paginate_by)
        context['movie_list'] = paginator.page(context['page_obj'].number)
        context['page_title'] = self.movie_list_page_title
        context['meta_content_description'] = self.content_metadescription
        return context


class MovieDetailView(generic.DetailView):
    model = Movie

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(MovieDetailView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        movie = Movie.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
        context['page_title'] = str(movie) + ' | The Horror Explosion'
        context['meta_content_description'] = \
            'Data and metadata about ' + str(movie) + ' like genre/subgenre ' \
            'affiliation and plot keywords'
        context['movie_directors'] = movie.return_mov_participation_data(
            'Director')
        context['movie_cast'] = movie.return_mov_participation_data('Actor')
        context['associated_reviews'] = movie.moviereview_set.all()
        referenced_in_reviews = ReferencedMovie.objects.filter(
            referenced_movie=movie)
        context['referenced_in_reviews'] = referenced_in_reviews
        return context


class MovieReviewListView(generic.ListView):
    model = MovieReview
    paginate_by = 5
    movie_review_list_page_title = "Movie Review List | The Horror Explosion"
    content_metadescription = "The list of all the movie reviews in our " \
                              "database."

    def get_context_data(self, **kwargs):
        context = super(MovieReviewListView, self).get_context_data(**kwargs)
        sorted_mov_reviews = sort_titles_with_stop_word(
            MovieReview.objects.all(), 'review')
        paginator = Paginator(sorted_mov_reviews, self.paginate_by)
        context['moviereview_list'] = paginator.page(
            context['page_obj'].number)
        context['page_title'] = self.movie_review_list_page_title
        context['meta_content_description'] = self.content_metadescription
        return context


class MovieReviewDetailView(generic.DetailView):
    model = MovieReview

    def get_context_data(self, **kwargs):
        context = super(MovieReviewDetailView, self).get_context_data(**kwargs)
        movie_review = MovieReview.objects.get(pk=self.kwargs.get(
            self.pk_url_kwarg))
        context['page_title'] = str(movie_review.reviewed_movie) + \
            ' | Movie Review | The Horror Explosion'
        context['meta_content_description'] = movie_review.\
            mov_review_page_description
        context['movie'] = movie_review.reviewed_movie
        context['movie_directors'] = movie_review.reviewed_movie.\
            return_mov_participation_data('Director')
        context['movie_cast'] = \
            movie_review.reviewed_movie.return_mov_participation_data('Actor')
        return context
