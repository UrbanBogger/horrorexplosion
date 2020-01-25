import re
import html
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.db.models import Q
from reviews.models import Movie, ReferencedMovie, MovieReview

RELEASE_YEAR_REGEX = r'^\(([0-9]{4})\)$'
MOV_TITLE_REGEX = r'^([a-zA-Z0-9\s]+)$'
MOV_TITLE_AND_YEAR_REGEX = r'^([a-zA-Z0-9\s]+)\s?\(([0-9]{4})\)$'
MOV_TITLE_HTML_TAG_REGEX = r'<.*>([a-zA-Z0-9\s]+)<\/.*>'


def get_mov_title_and_year_from_link(link, mov_title_modified):
    mov_title = None
    release_year = None

    for link_txt in link.contents:
        if re.match(MOV_TITLE_REGEX, str(link_txt).strip()):
            if mov_title_modified in re.match(MOV_TITLE_REGEX,
                                              str(link_txt)).group(1).strip():
                mov_title = re.match(MOV_TITLE_REGEX,
                                     str(link_txt)).group(1).strip()

        if re.match(MOV_TITLE_AND_YEAR_REGEX, str(link_txt).strip()):
            if mov_title_modified in re.match(MOV_TITLE_AND_YEAR_REGEX,
                                              str(link_txt)).group(1).strip():
                mov_title = re.match(MOV_TITLE_AND_YEAR_REGEX,
                                     str(link_txt)).group(1).strip()

            release_year = re.match(MOV_TITLE_AND_YEAR_REGEX,
                                    str(link_txt).strip()).group(2).strip()

        if re.match(RELEASE_YEAR_REGEX, str(link_txt).strip()):
            release_year = re.match(RELEASE_YEAR_REGEX,
                                    str(link_txt).strip()).group(1).strip()

        if re.match(MOV_TITLE_HTML_TAG_REGEX, str(link_txt).strip()):
            mov_title = re.match(MOV_TITLE_HTML_TAG_REGEX,
                                 str(link_txt).strip()).group(1).strip()

    return mov_title, release_year


class Command(BaseCommand):
    help = 'Adds recently added Movies to the Referenced Movies DB table'

    def handle(self, *args, **options):
        all_movies = Movie.objects.values_list('id', flat=True).order_by(
            '-first_created')
        self.stdout.write('Beginning to add movies to Referenced Movies '
                          'DB table')

        for movie_id in all_movies:
            movie = Movie.objects.get(id=movie_id)
            all_mov_revs = MovieReview.objects.values_list(
                'id', flat=True).exclude(reviewed_movie=movie)
            mov_main_title_modified = str(movie.main_title).replace(
                '’', '').replace('\'', '')

            for mov_rev_id in all_mov_revs:
                mov_rev_txt_unescaped = html.unescape(MovieReview.objects.get(
                    id=mov_rev_id).review_text)
                mov_rev_txt_modified = mov_rev_txt_unescaped.replace(
                    '’', '').replace('\'', '')
                html_to_be_inspected = BeautifulSoup(mov_rev_txt_modified,
                                                     'html.parser')
                links = html_to_be_inspected.find_all('a')

                if ReferencedMovie.objects.filter(
                        Q(referenced_movie=movie) & Q(
                            review=mov_rev_id)).exists():
                    continue
                elif mov_main_title_modified in mov_rev_txt_modified:
                    for link in links:
                        mov_referenced = False
                        # check if link points to a IMDb Movie page
                        if 'title' in link.attrs['href']:
                            mov_title, release_year = \
                                get_mov_title_and_year_from_link(
                                    link, mov_main_title_modified)

                            if release_year == str(movie.year_of_release) \
                                    and mov_title == mov_main_title_modified:
                                mov_referenced = True

                            if mov_title == mov_main_title_modified and not \
                                    release_year:
                                mov_referenced = True

                        # update referenced mov object
                        if mov_referenced and ReferencedMovie.objects.filter(
                                review=mov_rev_id).exists():
                            ref_mov = ReferencedMovie.objects.filter(
                                review=mov_rev_id).get()
                            self.stdout.write(
                                'UPDATING Referenced Movie object for movie: '
                                '%s and movie review: %s' % (str(movie),
                                str(MovieReview.objects.get(id=mov_rev_id))))
                            ref_mov.referenced_movie.add(movie)
                        # create a new referenced movie object
                        elif mov_referenced:
                            self.stdout.write(
                                'CREATING Referenced Movie object for movie: '
                                '%s and movie review: %s' % (str(movie), str(
                                    MovieReview.objects.get(id=mov_rev_id))))
                            ref_mov = ReferencedMovie()
                            ref_mov.review = MovieReview.objects.get(
                                id=mov_rev_id)
                            ref_mov.save()
                            ref_mov.referenced_movie.add(movie)

        self.stdout.write(
            'Have finished adding entries for movies in the Referenced '
            'Movies DB table')
