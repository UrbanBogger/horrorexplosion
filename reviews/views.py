import sys
import re
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.views import generic
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import EmailMessage, BadHeaderError
from django.http import HttpResponse
from .forms import ContactForm
from .models import Movie, MovieReview, WebsiteMetadescriptor,ReferencedMovie, \
    Contributor, MovieRemake, MovieSeries, MovieInMovSeries, \
    SimilarMovie, get_random_review

# Create your views here.

ENGLISH_ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                    'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                    'W', 'X', 'Y', 'Z']
ORDERING_SEQUENCE = ['ascending', 'descending']
DEFAULT_ORDERING = 'alphabetical-ascending'
ITEMS_PER_PAGE = 25
MOV_ORDERING_DICT = {
    'alphabetical-ascending': ('title_for_sorting', '(by Title, Ascending)'),
    'alphabetical-descending': ('-title_for_sorting', '(by Title, '
                                                      'Descending)'),
    'date_added-ascending': ('first_created', '(by Date Added, Ascending)'),
    'date_added-descending': ('-first_created', '(by Date Added, Descending)'),
    'release_year-ascending': ('year_of_release', '(by Release Year, '
                                                  'Ascending)'),
    'release_year-descending': ('-year_of_release', '(by Release Year, '
                                                    'Descending)')
}
MOV_ORDERING_CATEGORIES = ['alphabetical', 'date_added', 'release_year']
MOVREV_ORDERING_DICT = {
    'alphabetical-ascending': ('reviewed_movie', '(by Title, Ascending)'),
    'alphabetical-descending': ('-reviewed_movie', '(by Title, Descending)'),
    'date_added-ascending': ('first_created', '(by Date Added, Ascending)'),
    'date_added-descending': ('-first_created', '(by Date Added, Descending)'),
    'rating-ascending': ('grade', '(by Rating, Ascending)'),
    'rating-descending': ('-grade', '(by Rating, Descending)'),
    'author-ascending': ('review_author', '(by Author, Ascending)'),
    'author-descending': ('-review_author', '(by Author, Descending)')
}
MOVREV_ORDERING_CATEGORIES = ['alphabetical', 'date_added', 'rating',
                              'author']


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
            if Movie.objects.filter( main_title__title=mov_title,
                                     year_of_release=mov_year).exists():
                mov_title_link['href'] = Movie.objects.filter(
                    main_title__title=mov_title,
                    year_of_release=mov_year).order_by('year_of_release')[
                    0].get_absolute_url()

        else:
            if Movie.objects.filter(
                    main_title__title=mov_title).exists():
                mov_title_link['href'] = Movie.objects.filter(
                    main_title__title=mov_title).order_by(
                    'year_of_release')[0].get_absolute_url()

    return str(html_to_be_modified)


def get_mov_title_and_release_year(mov_link):
    mov_title_w_year_pattern = re.compile(r'.+\([0-9]{4}\).*')
    mov_year_split_pattern = re.compile(r'\([0-9]{4}\)')
    mov_year_pattern = re.compile(r'\(([0-9]{4})\)')
    html_comment_pattern = re.compile(r'.*<!--.*-->.*')
    mov_title = ''
    mov_year = None

    if html_comment_pattern.match(str(mov_link)):
        html_comment_content = mov_link.contents[1].string.strip()
        if mov_title_w_year_pattern.match(html_comment_content):
            mov_title = mov_year_split_pattern.split(
                html_comment_content)[0].strip()
            mov_year = mov_year_pattern.search(
                html_comment_content).group(1)

        else:
            mov_title = html_comment_content

    elif mov_link.find('em'):
        mov_title = mov_link.find('em').string

        if len(mov_link.contents) == 2:
            if mov_year_pattern.match(mov_link.contents[1]):
                mov_year = mov_year_pattern.search(mov_link.contents[
                                                      1]).group(1)

    elif mov_title_w_year_pattern.match(mov_link.string):
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
    latest_review = MovieReview.objects.latest('id')
    random_review = get_random_review(latest_review)
    home_page_title = WebsiteMetadescriptor.objects.get().landing_page_title
    content_metadescription = WebsiteMetadescriptor. \
        objects.get().landing_page_description
    return render(request, 'index.html',
                  context={'page_title': home_page_title,
                           'meta_content_description': content_metadescription,
                           'number_of_reviews': number_of_reviews,
                           'number_of_movies': number_of_movies,
                           'latest_review': latest_review,
                           'random_review': random_review}, )


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

    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)

        if form.is_valid():
            contact_name = form.cleaned_data['contact_name']
            contact_email = form.cleaned_data['contact_email']
            content = form.cleaned_data['content']

            try:
                email = EmailMessage(contact_name, content, contact_email,
                                     ['thehorrorexplosion@gmail.com'],
                                     fail_silently=False,
                                     reply_to=[contact_email])
                sys.stdout.write('Email being sent...\n')
                sys.stdout.write('Name: "%s"\n' % contact_name)
                sys.stdout.write('Contact email: "%s"\n' % contact_email)
                sys.stdout.write('Content: "%s"\n' % content)
                email.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect(thanks)
    return render(request, 'contact.html',
                  context={'form': form, 'page_title': contact_page_title,
                           'meta_content_description': content_metadescription}
                  )

    '''
    return render(request, 'contact.html',
                  context={'page_title': contact_page_title,
                           'meta_content_description': content_metadescription}
                  )
    '''


def thanks(request):
    thanks_page_info = "Thank you | The Horror Explosion"
    content_metadescription = "The Horror Explosion's 'thank you' page"
    return render(request, 'thanks.html', context={
        'page_title': thanks_page_info,
        'meta_content_description': content_metadescription})


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


def process_ordering_req(ordering_request, ordering_dict, ordering_categories):
    if not ordering_request:
        ordering_request = ['alphabetical', 'ascending']
    elif len(ordering_request) == 1:
        if ordering_request[0] in ordering_categories:
            ordering_request.insert(1, 'ascending')
        elif ordering_request[0] in ORDERING_SEQUENCE:
            ordering_request.insert(0, 'alphabetical')
        else:
            ordering_request = ['alphabetical', 'ascending']

    if ordering_dict.get('-'.join(ordering_request)):
        ordering = '-'.join(ordering_request)
    else:
        ordering = DEFAULT_ORDERING
        ordering_request = ['alphabetical', 'ascending']

    return ordering, ordering_request


def paginate_qs(qs, page):
    paginator = Paginator(qs, ITEMS_PER_PAGE)

    try:
        paginated_qs = paginator.page(page)
    except PageNotAnInteger:
        paginated_qs = paginator.page(1)
    except EmptyPage:
        paginated_qs = paginator.page(paginator.num_pages)

    return paginated_qs


def orderable_movie_list(request):
    movie_list_page_title = "Movie List | The Horror Explosion"
    content_metadescription = "The list of all the movies in our database."

    ordering_req = (request.GET.getlist('ordering'))
    ordering, ordering_req = process_ordering_req(
        ordering_req, MOV_ORDERING_DICT, MOV_ORDERING_CATEGORIES)
    ordering_msg = MOV_ORDERING_DICT.get(ordering)[1]

    mov_qs = Movie.objects.all().order_by(MOV_ORDERING_DICT.get(ordering)[0],
                                          'title_for_sorting')
    page = request.GET.get('page', 1)
    movies = paginate_qs(mov_qs, page)

    return render(request, 'movie_list.html',
                  {'page_title': movie_list_page_title,
                   'meta_content_description': content_metadescription,
                   'movie_list': movies, 'ordering_category': ordering_req[0],
                   'ordering_sequence': ordering_req[1],
                   'ordering_msg': ordering_msg})


def orderable_movreview_list(request):
    movie_list_page_title = "Movie Review List | The Horror Explosion"
    content_metadescription = "The list of all the movie reviews in our " \
                              "database."

    ordering_req = (request.GET.getlist('ordering'))
    ordering, ordering_req = process_ordering_req(
        ordering_req, MOVREV_ORDERING_DICT, MOVREV_ORDERING_CATEGORIES)
    ordering_msg = MOVREV_ORDERING_DICT.get(ordering)[1]

    movrev_qs = MovieReview.objects.all().order_by(
        MOVREV_ORDERING_DICT.get(ordering)[0], 'reviewed_movie')
    page = request.GET.get('page', 1)
    movreviews = paginate_qs(movrev_qs, page)

    return render(request, 'movreview_list.html',
                  {'page_title': movie_list_page_title,
                   'meta_content_description': content_metadescription,
                   'review_list': movreviews,
                   'ordering_category': ordering_req[0],
                   'ordering_sequence': ordering_req[1],
                   'ordering_msg': ordering_msg})


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


def get_preceding_and_following_movies(movie):
    preceding_mov = None
    following_mov = None

    if MovieSeries.objects.filter(mov_series__movie_in_series=movie).exists():
        relevant_mov_series = MovieSeries.objects.get(
            mov_series__movie_in_series=movie)
        mov_position_in_series = relevant_mov_series.mov_series.get(
            movie_in_series=movie).position_in_series

        try:
            preceding_mov = relevant_mov_series.mov_series.get(
                position_in_series=mov_position_in_series - 1).movie_in_series
        except MovieInMovSeries.DoesNotExist:
            pass

        try:
            following_mov = relevant_mov_series.mov_series.get(
                position_in_series=mov_position_in_series + 1).movie_in_series
        except MovieInMovSeries.DoesNotExist:
            pass

    return preceding_mov, following_mov


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
        if MovieRemake.objects.filter(remade_movie=movie).exists():
            remakes = MovieRemake.objects.get(remade_movie=movie).remake.all()
            context['remakes'] = remakes
        if MovieRemake.objects.filter(remake=movie).exists():
            original_mov = MovieRemake.objects.get(remake=movie).remade_movie
            context['remade_movie'] = original_mov
        preceding_mov, following_mov = get_preceding_and_following_movies(
            movie)
        context['preceding_movie'] = preceding_mov
        context['following_movie'] = following_mov
        context['similar_movies'] = SimilarMovie.objects.filter(
            compared_mov=Movie.objects.get(
                pk=self.kwargs.get(self.pk_url_kwarg))).order_by(
            '-overall_similarity_percentage')
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
