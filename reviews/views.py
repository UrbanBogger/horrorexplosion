import sys
import re
import random
from bs4 import BeautifulSoup
from operator import itemgetter
from django.shortcuts import render, redirect
from django.views import generic
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import EmailMessage, BadHeaderError
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.contrib.sites.models import Site
from .forms import ContactForm
from .google_structured_data import mov_review_sd, tv_episode_rev_sd, mov_sd
from .models import Movie, MovieReview, WebsiteMetadescriptor, \
    ReferencedMovie, Contributor, MovieRemake, MovieSeries, MovieInMovSeries, \
    SimilarMovie, PickedReview, TelevisionSeries, TelevisionSeason, \
    TelevisionEpisode, TelevisionSeasonReview, TelevisionEpisodeReview, \
    MovieFranchise, MovSeriesEntry, MovieCreator, DefaultImage, Subgenre, \
    Microgenre, Keyword, get_random_review, return_mov_participation_data

# Create your views here.
HTTP_PROTOCOL = 'http://'
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


def get_absolute_url(db_object):
    absolute_url = '{http}{domain}{object_url}'.format(
        http=HTTP_PROTOCOL, domain=Site.objects.get_current().domain,
        object_url=db_object.get_absolute_url())
    return absolute_url


def substitute_links_in_text(text):
    mov_title_pattern = re.compile(r'.*imdb.*/title/')
    html_to_be_modified = BeautifulSoup(text, 'html.parser')
    links = html_to_be_modified.find_all('a')

    if not links:
        return text

    mov_franchise_links = list(
        filter(bool, [link if 'franchise' in link.attrs.get(
            'href') or 'film_series' in link.attrs.get(
            'href') else '' for link in links]))

    if mov_franchise_links:
        franchise_name = None
        for mf_link in mov_franchise_links:
            mf_matches = re.findall(
                r'(.+?)_\(franchise\)|(.+?)_\(film_series\)',
                mf_link.attrs.get('href').split('/')[-1])

            if mf_matches:
                # access the franchise name tuple
                if mf_matches[0][0]:
                    franchise_name = mf_matches[0][0].replace('_', ' ')
                else:
                    franchise_name = mf_matches[0][1].replace('_', ' ')

            if franchise_name:
                if MovieFranchise.objects.filter(
                        franchise_name__contains=franchise_name).exists():
                    mov_franchise = MovieFranchise.objects.get(
                        franchise_name__contains=franchise_name)
                    if mov_franchise.is_publishable:
                        mf_link['href'] = mov_franchise.get_absolute_url()

    mov_title_links = list(filter(
        bool, [mov_title_link if mov_title_pattern.match(
            mov_title_link.attrs.get('href')) else '' for mov_title_link in
               links]))

    if not mov_title_links:
        return str(html_to_be_modified)

    for mov_title_link in mov_title_links:
        mov_title, mov_year = get_mov_title_and_release_year(mov_title_link)

        if mov_year:
            if Movie.objects.filter(main_title__title=mov_title,
                                    year_of_release=mov_year).exists():
                mov_title_link['href'] = Movie.objects.filter(
                    main_title__title=mov_title,
                    year_of_release=mov_year).order_by('year_of_release')[
                    0].get_absolute_url()
            elif TelevisionSeries.objects.filter(
                    main_title__title=mov_title).exists():
                mov_title_link['href'] = TelevisionSeries.objects.filter(
                    main_title__title=mov_title)[0].get_absolute_url()
            elif TelevisionEpisodeReview.objects.filter(
                    reviewed_tv_episode__episode_title=mov_title,
                    reviewed_tv_episode__tv_season__year_of_release=mov_year
            ).exists():
                mov_title_link['href'] = \
                    TelevisionEpisodeReview.objects.filter(
                        reviewed_tv_episode__episode_title=mov_title)[0].\
                        get_absolute_url()
            elif MovSeriesEntry.objects.filter(
                    mov_in_series_title__title=mov_title,
                    year_of_release=mov_year).exists():
                series_entry = MovSeriesEntry.objects.filter(
                    mov_in_series_title__title=mov_title,
                    year_of_release=mov_year).get()
                associated_franchises = [
                    franchise for franchise in
                    series_entry.franchise_association.all() if
                    franchise.is_publishable]
                if associated_franchises:
                    mov_title_link['href'] = \
                        associated_franchises[0].get_absolute_url() + '#' \
                        + str(''.join(
                            series_entry.mov_in_series_title.title.split()))

        else:
            if Movie.objects.filter(
                    main_title__title=mov_title).exists():
                mov_title_link['href'] = Movie.objects.filter(
                    main_title__title=mov_title).order_by(
                    'year_of_release')[0].get_absolute_url()
            elif TelevisionSeries.objects.filter(
                    main_title__title=mov_title).exists():
                mov_title_link['href'] = TelevisionSeries.objects.filter(
                    main_title__title=mov_title)[0].get_absolute_url()
            elif TelevisionEpisodeReview.objects.filter(
                    reviewed_tv_episode__episode_title=mov_title).exists():
                mov_title_link['href'] = \
                    TelevisionEpisodeReview.objects.filter(
                        reviewed_tv_episode__episode_title=mov_title)[0].\
                        get_absolute_url()
            elif MovSeriesEntry.objects.filter(
                    mov_in_series_title__title=mov_title).exists():
                series_entry = MovSeriesEntry.objects.filter(
                    mov_in_series_title__title=mov_title).get()
                associated_franchises = [
                    franchise for franchise in
                    series_entry.franchise_association.all() if
                    franchise.is_publishable]
                if associated_franchises:
                    mov_title_link['href'] = \
                        associated_franchises[0].get_absolute_url() + '#' \
                        + str(''.join(
                            series_entry.mov_in_series_title.title.split()))
            # to catch franchises mentioned in comments
            elif MovieFranchise.objects.filter(
                    franchise_name__icontains=mov_title).exists():
                mov_franchise = MovieFranchise.objects.get(
                    franchise_name__icontains=mov_title)
                if mov_franchise.is_publishable:
                    mov_title_link['href'] = mov_franchise.get_absolute_url()

    return str(html_to_be_modified)


def get_mov_title_and_release_year(mov_link):
    mov_title_w_year_pattern = re.compile(r'.+\([0-9]{4}\).*')
    mov_year_split_pattern = re.compile(r'\([0-9]{4}\)')
    mov_year_pattern = re.compile(r'\(([0-9]{4})\)')
    html_comment_pattern = re.compile(r'.*<!--.*-->.*')
    mov_title = ''
    mov_year = None

    if html_comment_pattern.match(str(mov_link)):
        html_comment_content = mov_link.contents[-1].string.strip()
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
            if mov_year_pattern.match(mov_link.contents[-1].strip()):
                mov_year = mov_year_pattern.search(
                    mov_link.contents[-1]).group(1)

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
    num_of_tv_season_reviews = TelevisionSeasonReview.objects.all().count()
    num_of_tv_episode_reviews = TelevisionEpisodeReview.objects.all().count()
    num_of_tv_reviews = num_of_tv_season_reviews + num_of_tv_episode_reviews
    latest_mov_review = MovieReview.objects.latest('id')
    try:
        featured_review = PickedReview.objects.latest('id').picked_review
    except PickedReview.DoesNotExist:
        featured_review = None
    random_review = get_random_review(latest_mov_review, featured_review)
    latest_tv_review = None
    try:
        latest_tvepisode_review = TelevisionEpisodeReview.objects.latest('id')
    except TelevisionEpisodeReview.DoesNotExist:
        latest_tvepisode_review = None
    try:
        latest_tvseason_review = TelevisionSeasonReview.objects.latest('id')
    except TelevisionSeasonReview.DoesNotExist:
        latest_tvseason_review = None

    if not latest_tvepisode_review or not latest_tvseason_review:
        if latest_tvepisode_review:
            latest_tv_review = latest_tvepisode_review
        elif latest_tvseason_review:
            latest_tv_review = latest_tvseason_review
    else:
        if latest_tvepisode_review.first_created > \
                latest_tvseason_review.first_created:
            latest_tv_review = latest_tvepisode_review
        elif latest_tvepisode_review.first_created == \
                latest_tvseason_review.first_created:
            if random.getrandbits(1):
                latest_tv_review = latest_tvepisode_review
            else:
                latest_tv_review = latest_tvseason_review
        else:
            latest_tv_review = latest_tvseason_review

    latest_review = None
    second_latest_review = None

    if latest_tv_review.first_created > latest_mov_review.first_created:
        latest_review = ("Latest TV Series Review", latest_tv_review)
        second_latest_review = ("Latest Film Review", latest_mov_review)
    else:
        latest_review = ("Latest Film Review", latest_mov_review)
        second_latest_review = ("Latest TV Series Review", latest_tv_review)

    home_page_title = WebsiteMetadescriptor.objects.get().landing_page_title
    content_metadescription = WebsiteMetadescriptor. \
        objects.get().landing_page_description
    intro_txt = WebsiteMetadescriptor.objects.get().landing_page_intro_txt
    return render(request, 'index.html',
                  context={'page_title': home_page_title,
                           'meta_content_description': content_metadescription,
                           'intro_txt': intro_txt,
                           'number_of_reviews': number_of_reviews,
                           'num_of_tv_reviews': num_of_tv_reviews,
                           'number_of_movies': number_of_movies,
                           'latest_review': latest_review,
                           'second_latest_review': second_latest_review,
                           'random_review': random_review,
                           'featured_review': featured_review,
                           'latest_tv_review': latest_tv_review},)


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
                           'meta_content_description':
                               content_metadescription})


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


def creator_index(request, first_letter=''):
    creator_index_page_title = "Creator Index | The Horror Explosion"
    content_metadescription = 'An alphabetical index of the movie creators ' \
                              'in our database'
    all_creators = MovieCreator.objects.all()
    creator_dict_list = []

    for creator in all_creators:
        primary_orderable_name = ''
        secondary_orderable_name = ''
        tertiary_orderable_name = ''

        if creator.last_name:
            primary_orderable_name = str(creator.last_name)
        else:
            primary_orderable_name = str(creator.first_name)

        if creator.first_name and creator.last_name:
            secondary_orderable_name = creator.first_name

        tertiary_orderable_name = creator.middle_name

        if creator.first_name and creator.last_name:
            display_name = '{last_name}, {first_name} {middle_name}'.format(
                last_name=str(creator.last_name),
                first_name=str(creator.first_name),
                middle_name=str(creator.middle_name))
        else:
            display_name = '{last_name}'.format(
                last_name=primary_orderable_name)

        creator_dict = {'primary_orderable_name': primary_orderable_name,
                        'secondary_orderable_name': secondary_orderable_name,
                        'tertiary_orderable_name': tertiary_orderable_name,
                        'display_name': display_name.strip(),
                        'creator_link': creator.get_absolute_url()}
        creator_dict_list.append(creator_dict)

    creator_dict_list.sort(
        key=itemgetter('primary_orderable_name', 'secondary_orderable_name',
                       'tertiary_orderable_name'))

    letter_creator_dict = {}
    if not first_letter:
        for letter in ENGLISH_ALPHABET:
            letter_creator_dict[letter] = [
                creator_dict['display_name'] for creator_dict in
                creator_dict_list if
                creator_dict['primary_orderable_name'][0] == letter]

    creators_per_letter = {}
    creators = []
    if first_letter:
        creators = [
            creator_dict for creator_dict in creator_dict_list if
            creator_dict['primary_orderable_name'][0] == first_letter]
        creators_per_letter[first_letter] = creators

    if not letter_creator_dict:
        letter_creator_dict = None

    if not creators_per_letter:
        creators_per_letter = None

    return render(request, 'creator-index.html',
                  context={
                      'page_title': creator_index_page_title,
                      'meta_content_description': content_metadescription,
                      'creators_dict': letter_creator_dict,
                      'creators_per_letter': creators_per_letter})


def keyword_index(request, first_letter=''):
    kw_index_page_title = "Keyword Index | The Horror Explosion"
    content_metadescription = 'An alphabetical list of the keywords in our ' \
                              'database'
    all_keywords = Keyword.objects.all()
    keywords_per_letter = {}
    letter_keyword_dict = {}

    for letter in ENGLISH_ALPHABET:
        letter_keyword_dict[letter] = all_keywords.filter(
            name__istartswith=letter)

    if first_letter:
        keywords_per_letter[first_letter] = letter_keyword_dict.get(
            first_letter)

    return render(request, 'keyword-index.html',
                  context={
                      'page_title': kw_index_page_title,
                      'meta_content_description': content_metadescription,
                      'kw_dict': letter_keyword_dict,
                      'keywords_per_letter': keywords_per_letter})


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


def orderable_tvseriesreview_list(request):
    tv_series_review_list = "TV Series Review List | The Horror Explosion"
    content_metadescription = "The list of all TV series reviews in our " \
                              "database"

    all_tv_series = TelevisionSeries.objects.all()
    tv_season_revs = [(tv_series.title_for_sorting, tv_season_rev)
                      for tv_series in all_tv_series
                      for tv_season in tv_series.televisionseason_set.all()
                      for tv_season_rev in
                      tv_season.televisionseasonreview_set.all()]
    tv_episode_revs = [(tv_series.title_for_sorting, tv_episode_rev) for
                       tv_series in all_tv_series for tv_season in
                       tv_series.televisionseason_set.all() for tv_episode in
                       tv_season.televisionepisode_set.all() for
                       tv_episode_rev in
                       tv_episode.televisionepisodereview_set.all()]

    all_tv_revs_sorted = [tv_rev_tuple[1] for tv_rev_tuple in
                          sorted(tv_season_revs + tv_episode_revs,
                                 key=itemgetter(0))]

    tv_series_revs = []
    for tv_rev in all_tv_revs_sorted:
        season_thumb = None
        season_poster = None
        series_thumb = None
        series_poster = None
        episode_thumb = None
        episode_poster = None
        try:
            if tv_rev.reviewed_tv_season:
                if tv_rev.reviewed_tv_season.poster_thumbnail:
                    season_thumb = tv_rev.reviewed_tv_season.poster_thumbnail
                elif tv_rev.reviewed_tv_season.poster:
                    season_poster = tv_rev.reviewed_tv_season.poster
                elif tv_rev.reviewed_tv_season.tv_series.poster_thumbnail:
                    series_thumb = \
                        tv_rev.reviewed_tv_season.tv_series.poster_thumbnail
                else:
                    series_poster = tv_rev.reviewed_tv_season.tv_series.poster
        except AttributeError:
            pass
        try:
            if tv_rev.reviewed_tv_episode:
                if tv_rev.reviewed_tv_episode.poster_thumbnail:
                    episode_thumb = tv_rev.reviewed_tv_episode.poster_thumbnail
                elif tv_rev.reviewed_tv_episode.poster:
                    episode_poster = tv_rev.reviewed_tv_episode.poster
                elif tv_rev.reviewed_tv_episode.tv_season.tv_series.\
                        poster_thumbnail:
                    series_thumb = tv_rev.reviewed_tv_episode.tv_season.\
                        tv_series.poster_thumbnail
                else:
                    series_poster = tv_rev.reviewed_tv_episode.tv_season.\
                        tv_series.poster
        except AttributeError:
            pass

        mov_rev_dict = {'rev_name': str(tv_rev),
                        'rev_link': tv_rev.get_absolute_url(),
                        'rev_summary': tv_rev.mov_review_page_description,
                        'season_thumb': season_thumb,
                        'season_poster': season_poster,
                        'episode_thumb': episode_thumb,
                        'episode_poster': episode_poster,
                        'series_thumb': series_thumb,
                        'series_poster': series_poster,
                        'grade': tv_rev.grade}
        tv_series_revs.append(mov_rev_dict)

    page = request.GET.get('page', 1)
    tvseriesreviews = paginate_qs(tv_series_revs, page)

    return render(request, 'tv_series_review_list.html',
                  {'page_title': tv_series_review_list,
                   'meta_content_description': content_metadescription,
                   'review_list': tvseriesreviews})


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
    preceding_mov = []
    following_mov = []
    mov_franchises = None

    if MovSeriesEntry.objects.filter(movie_in_series=movie).exists():
        mov_series_entry = MovSeriesEntry.objects.filter(
            movie_in_series=movie)[0]
        mov_franchises = [
            mov_franchise for mov_franchise in
            mov_series_entry.franchise_association.all()]
        movs_position_in_series = mov_series_entry.position_in_series

        for mov_franchise in mov_franchises:
            entries_in_franchise = MovSeriesEntry.objects.filter(
                franchise_association=mov_franchise).all()

            if entries_in_franchise.filter(
                    position_in_series=movs_position_in_series - 1).exists() \
                    and entries_in_franchise.filter(
                position_in_series=movs_position_in_series - 1).get(). \
                    movie_in_series:
                pm = entries_in_franchise.filter(
                    position_in_series=movs_position_in_series - 1).get(). \
                    movie_in_series
                preceding_mov.append(pm)

            if entries_in_franchise.filter(
                    position_in_series=movs_position_in_series + 1).exists() \
                    and entries_in_franchise.filter(
                position_in_series=movs_position_in_series + 1).get(). \
                    movie_in_series:
                fv = entries_in_franchise.filter(
                    position_in_series=movs_position_in_series + 1).get(). \
                    movie_in_series
                following_mov.append(fv)

    if MovieSeries.objects.filter(mov_series__movie_in_series=movie).exists():
        relevant_mov_series = MovieSeries.objects.get(
            mov_series__movie_in_series=movie)
        mov_position_in_series = relevant_mov_series.mov_series.get(
            movie_in_series=movie).position_in_series

        try:
            pm = relevant_mov_series.mov_series.get(
                position_in_series=mov_position_in_series - 1).movie_in_series
            preceding_mov.append(pm)
        except MovieInMovSeries.DoesNotExist:
            pass

        try:
            fm = relevant_mov_series.mov_series.get(
                position_in_series=mov_position_in_series + 1).movie_in_series
            following_mov.append(fm)
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
        alt_durations_str = ''
        if movie.alternative_duration.all().exists():
            alt_durations_str = '/{alt_durations}'.format(
                alt_durations='/'.join(
                    str(alt_duration) for alt_duration in
                    movie.alternative_duration.all()))
        if movie.imdb_link:
            context['mov_sd'] = mov_sd(movie)
        context['page_title'] = str(movie) + ' | The Horror Explosion'
        context['meta_content_description'] = movie.get_meta_string()
        context['movie_directors'] = return_mov_participation_data(movie,
                                                                   'Director')
        context['movie_cast'] = return_mov_participation_data(movie, 'Actor')
        context['associated_reviews'] = movie.moviereview_set.all()
        associated_franchises = None
        if MovSeriesEntry.objects.filter(movie_in_series=movie).exists():
            series_entry = MovSeriesEntry.objects.filter(
                movie_in_series=movie).get()
            associated_franchises = [
                franchise for franchise in
                series_entry.franchise_association.all() if
                franchise.is_publishable]
            if associated_franchises and series_entry.short_review:
                context['short_review'] = (
                    ''.join(str(movie.main_title).split()),
                    associated_franchises)
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
        context['mov_franchise'] = associated_franchises
        context['following_movie'] = following_mov
        context['similar_movies'] = SimilarMovie.objects.filter(
            compared_mov=Movie.objects.get(
                pk=self.kwargs.get(self.pk_url_kwarg))).order_by(
            '-overall_similarity_percentage')
        context['alt_durations'] = alt_durations_str
        return context


class MovieReviewDetailView(generic.DetailView):
    model = MovieReview

    def get_context_data(self, **kwargs):
        context = super(MovieReviewDetailView, self).get_context_data(**kwargs)
        movie_review = MovieReview.objects.get(pk=self.kwargs.get(
            self.pk_url_kwarg))
        if movie_review.reviewed_movie.imdb_link and \
                movie_review.review_snippet:
            context['mov_rev_sd'] = mov_review_sd(
                movie_review,
                db_object_absolute_url=get_absolute_url(movie_review))
        alt_durations_str = ''
        if movie_review.reviewed_movie.alternative_duration.all().exists():
            alt_durations_str = '/{alt_durations}'.format(
                alt_durations='/'.join(
                    str(alt_duration) for alt_duration in
                    movie_review.reviewed_movie.alternative_duration.all()))
        context['review_text'] = substitute_links_in_text(
            movie_review.review_text)
        context['page_title'] = str(movie_review.reviewed_movie) + \
            ' | Movie Review | The Horror Explosion'
        context['meta_content_description'] = movie_review.\
            mov_review_page_description
        context['movie'] = movie_review.reviewed_movie
        context['movie_directors'] = return_mov_participation_data(
            movie_review.reviewed_movie, 'Director')
        context['movie_cast'] = return_mov_participation_data(
            movie_review.reviewed_movie, 'Actor')
        context['absolute_uri'] = get_absolute_url(movie_review)
        context['alt_durations'] = alt_durations_str
        return context


class TVSeriesListView(generic.ListView):
    model = TelevisionSeries
    tv_series_list_page_title = 'TV Series | The Horror Explosion'
    tv_series_metadescriptor = 'The list of TV series in our database'

    def get_context_data(self, **kwargs):
        context = super(TVSeriesListView, self).get_context_data(**kwargs)
        context['page_title'] = self.tv_series_list_page_title
        context['meta_content_description'] = self.tv_series_metadescriptor
        return context


class TVSeriesDetailView(generic.DetailView):
    model = TelevisionSeries

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(TVSeriesDetailView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        tv_series = TelevisionSeries.objects.get(pk=self.kwargs.get(
            self.pk_url_kwarg))
        context['page_title'] = str(tv_series) + ' | The Horror Explosion'
        context['meta_content_description'] = tv_series.get_meta_string()
        context['seasons'] = tv_series.televisionseason_set.all()
        context['tvseries_description'] = substitute_links_in_text(
            tv_series.description)
        return context


class TVSeasonDetailView(generic.DetailView):
    model = TelevisionSeason

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(TVSeasonDetailView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        tv_season = TelevisionSeason.objects.get(pk=self.kwargs.get(
            self.pk_url_kwarg))
        context['page_title'] = str(tv_season) + ' | The Horror Explosion'
        context['meta_content_description'] = tv_season.get_meta_string()
        context['directors'] = return_mov_participation_data(tv_season,
                                                             'Director')
        context['showrunners'] = return_mov_participation_data(
            tv_season, 'Showrunner')
        context['cast'] = return_mov_participation_data(tv_season, 'Actor')
        context['episode_durations'] = tv_season.get_episode_durations()
        return context


class TVSeasonReviewDetailView(generic.DetailView):
    model = TelevisionSeasonReview

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(TVSeasonReviewDetailView, self).get_context_data(
            **kwargs)
        # Create any data and add it to the context
        tv_season_review = TelevisionSeasonReview.objects.get(
            pk=self.kwargs.get(self.pk_url_kwarg))
        context['page_title'] = str(tv_season_review) \
                                + ' | The Horror Explosion'
        context['meta_content_description'] = \
            tv_season_review.mov_review_page_description
        context['directors'] = return_mov_participation_data(
            tv_season_review.reviewed_tv_season, 'Director')
        context['showrunners'] = return_mov_participation_data(
            tv_season_review.reviewed_tv_season, 'Showrunner')
        context['cast'] = return_mov_participation_data(
            tv_season_review.reviewed_tv_season, 'Actor')
        context['tvseason_review'] = substitute_links_in_text(
            tv_season_review.review_text)
        context['absolute_uri'] = get_absolute_url(tv_season_review)
        return context


class TVEpisodeReviewDetailView(generic.DetailView):
    model = TelevisionEpisodeReview

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(TVEpisodeReviewDetailView, self).get_context_data(
            **kwargs)
        # Create any data and add it to the context
        tv_episode_review = TelevisionEpisodeReview.objects.get(
            pk=self.kwargs.get(self.pk_url_kwarg))
        if tv_episode_review.reviewed_tv_episode.tv_season.tv_series \
                .imdb_link and tv_episode_review.reviewed_tv_episode \
                .imdb_link and tv_episode_review.review_snippet:
            context['tv_ep_rev_sd'] = tv_episode_rev_sd(
                tv_episode_review,
                db_object_absolute_url=get_absolute_url(tv_episode_review))
        context['page_title'] = str(tv_episode_review) \
                                + ' | The Horror Explosion'
        context['meta_content_description'] = \
            tv_episode_review.mov_review_page_description
        context['directors'] = return_mov_participation_data(
            tv_episode_review.reviewed_tv_episode, 'Director')
        context['cast'] = return_mov_participation_data(
            tv_episode_review.reviewed_tv_episode, 'Actor')
        context['tvepisode_review'] = substitute_links_in_text(
            tv_episode_review.review_text)
        context['absolute_uri'] = get_absolute_url(tv_episode_review)
        return context


class MovieFranchiseListView(generic.ListView):
    model = MovieFranchise
    mov_franchise_list_page_title = 'Horror Franchises | The Horror Explosion'
    mov_franchise_metadescriptor = 'The list of horror film franchises ' \
                                   'in our database'

    def get_context_data(self, **kwargs):
        context = super(
            MovieFranchiseListView, self).get_context_data(**kwargs)
        movie_franchises = MovieFranchise.objects.filter(is_publishable=True)
        context['moviefranchise_list'] = movie_franchises
        context['page_title'] = self.mov_franchise_list_page_title
        franchise_list = ','.join([str(mov_franchise) for mov_franchise
                                   in movie_franchises])
        context['meta_content_description'] = '{intro}:{list}'.format(
            intro=self.mov_franchise_metadescriptor, list=franchise_list)
        return context


class MovieFranchiseDetailView(generic.DetailView):
    model = MovieFranchise

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(MovieFranchiseDetailView, self).get_context_data(
            **kwargs)
        # Create any data and add it to the context
        mov_franchise = MovieFranchise.objects.get(pk=self.kwargs.get(
            self.pk_url_kwarg))
        if not mov_franchise.is_publishable:
            raise PermissionDenied
        all_entries = mov_franchise.movseriesentry_set.all()
        context['page_title'] = str(mov_franchise) + ' | The Horror Explosion'
        context['meta_content_description'] = \
            mov_franchise.get_metadata_string()
        context['franchise_entries'] = replace_links_in_franchise_entries(
            mov_franchise.movseriesentry_set.all())
        context['tv_series'] = [mov_series_entry.tv_series_entry for
                                mov_series_entry in all_entries
                                if mov_series_entry.tv_series_entry]
        return context


def create_mov_dict(film):
    image = None

    if film.poster:
        image = film.poster
    else:
        image = film.poster_thumbnail

    type = 'Full-length Film'
    genres = [str(genre) for genre in film.genre.all()]
    keywords = [str(keyword) for keyword in film.keyword.all()]

    if 'Animation' in genres and 'short film' in keywords:
        type = 'Animated Short'

    media_dict = {'media_object': film.get_absolute_url(),
                  'year': film.year_of_release,
                  'title': film.title_for_sorting,
                  'display_title': film.main_title,
                  'type': type,
                  'image': image}

    return media_dict


def create_tv_season_dict(tv_season):
    image = None

    if tv_season.poster_thumbnail:
        image = tv_season.poster_thumbnail
    elif tv_season.poster:
        image = tv_season.poster
    elif tv_season.tv_series.poster_thumbnail:
        image = tv_season.tv_series.poster_thumbnail

    else:
        image = tv_season.tv_series.poster

    if tv_season.year_of_release:
        year = tv_season.year_of_release
    else:
        year = None

    media_dict = {'media_object': tv_season.get_absolute_url(),
                  'year': year,
                  'season_number': tv_season.season_number,
                  'tv_episode_number': 0,
                  'title': tv_season.tv_series.title_for_sorting,
                  'display_title': str(tv_season),
                  'type': 'TV Series',
                  'image': image}
    return media_dict


def create_tv_episode_dict(tv_episode):
    image = None

    if tv_episode.poster_thumbnail:
        image = tv_episode.poster_thumbnail
    elif tv_episode.poster:
        image = tv_episode.poster

    elif tv_episode.tv_season.poster_thumbnail:
        image = tv_episode.tv_season.poster_thumbnail
    elif tv_episode.tv_season.poster:
        image = tv_episode.tv_season.poster
    elif tv_episode.tv_season.tv_series.poster_thumbnail:
        image = tv_episode.tv_season.tv_series.poster_thumbnail
    else:
        image = tv_episode.tv_season.tv_series.poster

    tv_episode_link = '#'

    if tv_episode.televisionepisodereview_set.all().exists():
        tv_episode_link = tv_episode.televisionepisodereview_set.all()[
            0].get_absolute_url()

    media_dict = {'media_object': tv_episode_link,
                  'title': tv_episode.tv_season.tv_series.title_for_sorting,
                  'display_title': str(tv_episode),
                  'year': tv_episode.tv_season.year_of_release,
                  'season_number': tv_episode.tv_season.season_number,
                  'tv_episode_number': tv_episode.episode_number,
                  'type': 'TV Series', 'image': image}

    return media_dict


class MovieCreatorDetailView(generic.DetailView):
    model = MovieCreator

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(MovieCreatorDetailView, self).get_context_data(
            **kwargs)
        mov_creator = MovieCreator.objects.get(pk=self.kwargs.get(
            self.pk_url_kwarg))
        mov_participations = mov_creator.movieparticipation_set.all()
        roles = list(set([mov_participation.creative_role for
                          mov_participation in mov_participations]))
        roles_updated = []

        roles_with_media_objects = []
        for role in roles:
            creators_film_roles = [
                mov_participation.movie_set.filter(
                    movie_participation__creative_role=role)
                for mov_participation in mov_participations
                if mov_participation.movie_set.filter(
                    movie_participation__creative_role=role).exists()]
            creators_tv_season_roles = [
                mov_participation.televisionseason_set.filter(
                    movie_participation__creative_role=role) for
                mov_participation in mov_participations
                if mov_participation.televisionseason_set.filter(
                    movie_participation__creative_role=role).exists()]
            creators_tv_episode_roles = [
                mov_participation.televisionepisode_set.filter(
                    movie_participation__creative_role=role)
                for mov_participation in mov_participations
                if mov_participation.televisionepisode_set.filter(
                    movie_participation__creative_role=role).exists()]
            media_objects_per_role = []
            if creators_film_roles:
                for qs in creators_film_roles:
                    for film in qs:
                        media_objects_per_role.append(create_mov_dict(film))
            if creators_tv_season_roles:
                for qs in creators_tv_season_roles:
                    for tv_season in qs:
                        media_objects_per_role.append(
                            create_tv_season_dict(tv_season))
            if creators_tv_episode_roles:
                for qs in creators_tv_episode_roles:
                    for tv_episode in qs:
                        media_objects_per_role.append(
                            create_tv_episode_dict(tv_episode))
            media_objects_per_role.sort(key=itemgetter('year', 'title'),
                                        reverse=True)

            if role.role_name.lower() == 'actor' and \
                    mov_creator.creator_sex == 'female':
                role_name = 'Actress'
            else:
                role_name = role.role_name
            role_and_media ={'role': role_name,
                             'media': media_objects_per_role}
            roles_with_media_objects.append(role_and_media)
        roles_with_media_objects.sort(key=itemgetter('role'))

        role_strings = [role.role_name for role in roles]
        for role in role_strings:
            if mov_creator.creator_sex == 'female' and role.lower() == 'actor':
                role = 'Actress'
                roles_updated.append(role)
            else:
                roles_updated.append(role)

        all_creative_roles = ', '.join([role for role
                                        in roles_updated])

        creator_img_styling = None
        if mov_creator.photograph:
            creator_img = mov_creator.photograph
            creator_img_styling = 'mov_creator_img_auto'
        elif mov_creator.creator_sex == 'female' \
                and DefaultImage.objects.filter(
            default_img_type='female').exists():
            creator_img = DefaultImage.objects.get(
                default_img_type='female').default_img
        elif DefaultImage.objects.filter(default_img_type='male').exists():
            creator_img = DefaultImage.objects.get(
                default_img_type='male').default_img
        if not creator_img_styling:
            creator_img_styling = 'mov_creator_poster'

        default_motion_pic_img = None
        if DefaultImage.objects.filter(
                default_img_type='motion_pic').exists():
            default_motion_pic_img = DefaultImage.objects.get(
                default_img_type='motion_pic').default_img

        context['page_title'] = str(mov_creator) + ' | The Horror Explosion'
        context['meta_content_description'] = \
            'Creator name:{name}|Creative Roles:{roles}'.format(
                name=str(mov_creator), roles=all_creative_roles)
        context['creative_roles'] = all_creative_roles
        context['creator_name'] = str(mov_creator)
        context['creator_img'] = creator_img
        context['creator_img_styling'] = creator_img_styling
        context['default_motion_pic_img'] = default_motion_pic_img
        context['filmography'] = roles_with_media_objects
        return context


def get_detailed_metadata(all_movs, all_tv_seasons, all_tv_episodes,
                          description_string_template):

    mov_dicts = []
    for mov in all_movs:
        mov_dicts.append(create_mov_dict(mov))
    mov_dicts.sort(key=itemgetter('title'))

    animated_shorts = None
    animated_shorts = list(filter(
        lambda film: film['type'] == 'Animated Short', mov_dicts))
    if animated_shorts:
        for animated_short in animated_shorts:
            mov_dicts.remove(animated_short)

    items_from_mov_dict = mov_dicts[:6]
    if items_from_mov_dict:
        mov_titles_sample = 'Films {description}{mov_sample}.'.format(
            description=description_string_template,mov_sample=','.join(
                str(film_dict['display_title']) for film_dict in
                items_from_mov_dict))
    else:
        mov_titles_sample = ''

    tv_series_dict = []
    for tv_season in all_tv_seasons:
        tv_series_dict.append(create_tv_season_dict(tv_season))

    for tv_episode in all_tv_episodes:
        tv_series_dict.append(create_tv_episode_dict(tv_episode))
    tv_series_dict.sort(key=itemgetter(
        'title', 'season_number', 'tv_episode_number'))

    items_from_tv_series_dict = tv_series_dict[:3]
    if items_from_tv_series_dict:
        tv_series_titles_sample = 'TV series {description}{tv_series}'.format(
            description=description_string_template, tv_series=','.join(
                str(tv_series_dict['display_title']) for tv_series_dict in
                items_from_tv_series_dict))
    else:
        tv_series_titles_sample = ''

    default_motion_pic_img = None
    if DefaultImage.objects.filter(default_img_type='motion_pic').exists():
        default_motion_pic_img = DefaultImage.objects.get(
            default_img_type='motion_pic').default_img

    return mov_dicts, tv_series_dict, animated_shorts, mov_titles_sample, \
           tv_series_titles_sample, default_motion_pic_img


def subgenre_detail_view(request, **kwargs):
    subgenre_pk = kwargs['pk']
    subgenre = Subgenre.objects.get(pk=subgenre_pk)
    all_movs = Movie.objects.filter(subgenre=subgenre)
    all_tv_seasons = TelevisionSeason.objects.filter(subgenre=subgenre)
    all_tv_episodes = TelevisionEpisode.objects.filter(subgenre=subgenre)

    mov_dicts, tv_series_dict, animated_shorts_dict, mov_titles_sample, \
    tv_series_titles_sample, default_motion_pic_img = get_detailed_metadata(
        all_movs, all_tv_seasons, all_tv_episodes,
        description_string_template='of the subgenre:')
    all_media_objects = mov_dicts + tv_series_dict + animated_shorts_dict

    page = request.GET.get('page', 1)
    all_media_objects = paginate_qs(all_media_objects, page)

    subgenre_detail_page_metadescriptor = \
        'Page for subgenre: "{mg}".{mov_sample_str}{tv_series_sample_str}'\
            .format(mg=str(subgenre), mov_sample_str=mov_titles_sample,
                    tv_series_sample_str=tv_series_titles_sample)
    subgenre_detail_page_title = \
        'Subgenre: "{sg}" | The Horror Explosion'.format(sg=str(subgenre))

    return render(request, 'subgenre_detail.html',
                  {'page_title': subgenre_detail_page_title,
                   'meta_content_description':
                       subgenre_detail_page_metadescriptor,
                   'all_media_objects': all_media_objects,
                   'subgenre': subgenre})

'''
class SubgenreDetailView(generic.DetailView):
    model = Subgenre

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(SubgenreDetailView, self).get_context_data(
            **kwargs)
        subgenre = Subgenre.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
        all_movs = Movie.objects.filter(subgenre=subgenre)
        all_tv_seasons = TelevisionSeason.objects.filter(subgenre=subgenre)
        all_tv_episodes = TelevisionEpisode.objects.filter(subgenre=subgenre)

        mov_dicts, tv_series_dict, animated_shorts_dict, mov_titles_sample, \
        tv_series_titles_sample, default_motion_pic_img = \
            get_detailed_metadata(
                all_movs, all_tv_seasons, all_tv_episodes,
                description_string_template='of the subgenre:')
        page_metadescriptor = \
            'Page for subgenre: "{mg}".{mov_sample_str}' \
            '{tv_series_sample_str}' \
            ''.format(mg=str(subgenre), mov_sample_str=mov_titles_sample,
                      tv_series_sample_str=tv_series_titles_sample)
        context['page_title'] = \
            'Subgenre: "{sg}" | The Horror Explosion'.format(sg=str(subgenre))
        context['meta_content_description'] = page_metadescriptor
        context['default_motion_pic_img'] = default_motion_pic_img
        context['features'] = mov_dicts
        context['tv_series'] = tv_series_dict
        context['animated_shorts'] = animated_shorts_dict
        return context
'''

class SubgenreListView (generic.ListView):
    model = Subgenre
    subgenres_page_title = "Subgenres | The Horror Explosion"
    content_metadescription = "The list of subgenres in our database"

    def get_context_data(self, **kwargs):
        context = super(SubgenreListView, self).get_context_data(**kwargs)
        context['page_title'] = self.subgenres_page_title
        context['meta_content_description'] = self.content_metadescription
        return context


class MicrogenreDetailView(generic.DetailView):
    model = Microgenre

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(MicrogenreDetailView, self).get_context_data(
            **kwargs)
        microgenre = Microgenre.objects.get(pk=self.kwargs.get(
            self.pk_url_kwarg))
        all_movs = Movie.objects.filter(microgenre=microgenre)
        all_tv_seasons = TelevisionSeason.objects.filter(microgenre=microgenre)
        all_tv_episodes = TelevisionEpisode.objects.filter(
            microgenre=microgenre)

        mov_dicts, tv_series_dict, animated_shorts_dict, mov_titles_sample, \
        tv_series_titles_sample, default_motion_pic_img = \
            get_detailed_metadata(
                all_movs, all_tv_seasons, all_tv_episodes,
                description_string_template='of the microgenre:')
        page_metadescriptor = \
            'Page for microgenre: "{mg}".{mov_sample_str}' \
            '{tv_series_sample_str}' \
            ''.format(mg=str(microgenre), mov_sample_str=mov_titles_sample,
                      tv_series_sample_str=tv_series_titles_sample)
        context['page_title'] = \
            'Microgenre: "{mg}" | The Horror Explosion'.format(mg=str(microgenre))
        context['meta_content_description'] = page_metadescriptor
        context['default_motion_pic_img'] = default_motion_pic_img
        context['features'] = mov_dicts
        context['tv_series'] = tv_series_dict
        context['animated_shorts'] = animated_shorts_dict
        return context


class MicrogenreListView (generic.ListView):
    model = Microgenre
    microgenres_page_title = "Microgenres | The Horror Explosion"
    content_metadescription = "The list of microgenres in our database"

    def get_context_data(self, **kwargs):
        context = super(MicrogenreListView, self).get_context_data(**kwargs)
        context['page_title'] = self.microgenres_page_title
        context['meta_content_description'] = self.content_metadescription
        return context


class KeywordDetailView(generic.DetailView):
    model = Keyword

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(KeywordDetailView, self).get_context_data(
            **kwargs)
        keyword = Keyword.objects.get(pk=self.kwargs.get(
            self.pk_url_kwarg))
        all_movs = Movie.objects.filter(keyword=keyword)
        all_tv_seasons = TelevisionSeason.objects.filter(keyword=keyword)
        all_tv_episodes = TelevisionEpisode.objects.filter(keyword=keyword)

        mov_dicts, tv_series_dict, animated_shorts_dict, mov_titles_sample, \
        tv_series_titles_sample, default_motion_pic_img = \
            get_detailed_metadata(
                all_movs, all_tv_seasons, all_tv_episodes,
                description_string_template='with the keyword:')
        page_metadescriptor = \
            'Page for keyword: "{kw}".{mov_sample_str}{tv_series_sample_str}' \
            ''.format(kw=str(keyword), mov_sample_str=mov_titles_sample,
                      tv_series_sample_str=tv_series_titles_sample)
        context['page_title'] = \
            'Keyword: "{kw}" | The Horror Explosion'.format(kw=str(keyword))
        context['meta_content_description'] = page_metadescriptor
        context['default_motion_pic_img'] = default_motion_pic_img
        context['features'] = mov_dicts
        context['tv_series'] = tv_series_dict
        context['animated_shorts'] = animated_shorts_dict
        return context


def replace_links_in_franchise_entries(franchise_entries):
    for franchise_entry in franchise_entries:
        if franchise_entry.short_review:
            franchise_entry.short_review = substitute_links_in_text(
                franchise_entry.short_review)
    return franchise_entries
