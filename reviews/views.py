import re
from bs4 import BeautifulSoup
from django.db.models.base import ObjectDoesNotExist
from django.shortcuts import render
from django.views import generic
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Movie, MovieReview, WebsiteMetadescriptor,ReferencedMovie, \
    Contributor, get_random_review

# Create your views here.

ENGLISH_ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                    'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                    'W', 'X', 'Y', 'Z']


def substitute_links_in_text(text):
    mov_title_pattern = re.compile(r'.*imdb.*/title/')
    html_to_be_modified = BeautifulSoup(text, 'html.parser')
    links = html_to_be_modified.find_all('a')

    if not links:
        return text

    mov_title_links = list(filter(
        bool, [mov_title_link if mov_title_pattern.match(
            mov_title_link.attrs.get('href')) else '' for mov_title_link in
               links]))

    if not mov_title_links:
        return text

    for mov_title_link in mov_title_links:
        mov_title, mov_year = get_mov_title_and_release_year(mov_title_link)
        if mov_year:
            try:
                mov = Movie.objects.get(
                    main_title__title__contains=mov_title,
                    year_of_release=mov_year)
            except ObjectDoesNotExist:
                continue

        else:
            try:
                mov = Movie.objects.get(main_title__title__contains=mov_title)
            except ObjectDoesNotExist:
                    continue
            mov_title_link['href'] = mov.get_absolute_url()
    return str(html_to_be_modified)


def get_mov_title_and_release_year(mov_link):
    mov_title_w_year_pattern = re.compile(r'.+\([0-9]{4}\).*')
    mov_year_split_pattern = re.compile(r'\([0-9]{4}\)')
    mov_year_pattern = re.compile(r'\(([0-9]{4})\)')
    mov_title = ''
    mov_year = None
    if mov_title_w_year_pattern.match(mov_link.string):
        mov_title = mov_year_split_pattern.split(
            mov_link.string)[0].strip()
        mov_year = mov_year_pattern.search(
            mov_link.string).group(1).strip()
    else:
        mov_title = mov_link.string.strip()
    if "’" in mov_title:
        mov_title = mov_title.replace("’", "'")
    return mov_title, mov_year


def index(request):
    number_of_reviews = MovieReview.objects.all().count()
    number_of_movies = Movie.objects.all().count()
    latest_review = MovieReview.objects.latest('first_created')
    random_review = get_random_review(latest_review)
    home_page_title = WebsiteMetadescriptor.objects.get().landing_page_title
    content_metadescription = WebsiteMetadescriptor.\
        objects.get().landing_page_description
    return render(request, 'index.html',
                  context={'page_title': home_page_title,
                           'meta_content_description': content_metadescription,
                           'number_of_reviews': number_of_reviews,
                           'number_of_movies': number_of_movies,
                           'latest_review': latest_review,
                           'random_review': random_review},)


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


def movie_index(request, first_letter=''):
    mov_index_page_title = "Movie Index | The Horror Explosion"
    content_metadescription = 'An alphabetical list of the movies in our ' \
                              'database'
    all_movies = Movie.objects.all()
    movies_per_letter = {}
    letter_movies_dict = {}
    for letter in ENGLISH_ALPHABET:
        letter_movies_dict[letter] = all_movies.filter(
            title_for_sorting__istartswith=letter)

    if first_letter:
        movies_per_letter[first_letter] = letter_movies_dict.get(first_letter)

    return render(request, 'movie-index.html',
                  context={
                      'page_title': mov_index_page_title,
                      'meta_content_description': content_metadescription,
                      'movie_dict': letter_movies_dict,
                      'movies_per_letter': movies_per_letter})


def orderable_movie_list(request):
    movie_list_page_title = "Movie List | The Horror Explosion"
    content_metadescription = "The list of all the movies in our database."
    ordering_dict = {'alphabetical':
                     ('title_for_sorting', '(by title)'),
                     'date_added':
                     ('first_created', '(by date of addition)'),
                     'release_year':
                     ('year_of_release', '(by release year)')}

    mov_qs = Movie.objects.all()
    ordering = request.GET.get('ordering')
    page = request.GET.get('page', 1)
    if ordering:
        mov_qs = Movie.objects.all().order_by(ordering_dict.get(ordering)[0])
    else:
        ordering = 'alphabetical'
    paginator = Paginator(mov_qs, 5)
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    return render(request, 'movie_list.html',
                  {'page_title': movie_list_page_title,
                   'meta_content_description': content_metadescription,
                   'movie_list': movies, 'current_ordering': ordering,
                   'ordering_msg': ordering_dict.get(ordering)[1]})


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
        context['page_title'] = self.movie_review_list_page_title
        context['meta_content_description'] = self.content_metadescription
        return context


class MovieReviewDetailView(generic.DetailView):
    model = MovieReview

    def get_context_data(self, **kwargs):
        context = super(MovieReviewDetailView, self).get_context_data(**kwargs)
        movie_review = MovieReview.objects.get(pk=self.kwargs.get(
            self.pk_url_kwarg))
        context['review_text'] = substitute_links_in_text(
            movie_review.review_text)
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
