import re
import html
from django.core.management.base import BaseCommand
from django.db.models import Q
from reviews.models import Movie, ReferencedMovie, MovieReview


MOV_TITLE_V1 = r'<a\s*href=\".*title.*\".*><em>?{mov_title}</em>?<\/a>'
MOV_TITLE_V2 = r'<!--\s?{mov_title}\s?.*-->'
YEAR_REGEX_V1 = r'<a\s*href=\".*title.*\".*>%s.*\(\s?([0-9]{4})\s?\)<\/a>'
YEAR_REGEX_V2 = r'<!--\s?%s\s*\(\s?([0-9]{4})\s?\)-->'
YEAR_REGEX_MATCH_GROUP_NR = 1


def does_release_year_match(movie, regex_pattern, main_title='', rev_txt=''):
    # extract and check year of release
    release_year_search = re.search(regex_pattern % main_title, rev_txt,
                                    re.MULTILINE)
    if release_year_search:
        year = int(release_year_search.group(YEAR_REGEX_MATCH_GROUP_NR))
        if movie.year_of_release == year:
            return True
    else:
        return False


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
                mov_referenced = False
                mov_rev_txt_unescaped = html.unescape(MovieReview.objects.get(
                    id=mov_rev_id).review_text)
                mov_rev_txt_modified = mov_rev_txt_unescaped.replace(
                    '’', '').replace('\'', '')

                if ReferencedMovie.objects.filter(
                        Q(referenced_movie=movie) & Q(
                            review=mov_rev_id)).exists():
                    continue
                elif re.search(YEAR_REGEX_V1 % mov_main_title_modified,
                               mov_rev_txt_modified, re.MULTILINE):
                    mov_referenced = does_release_year_match(
                        movie, YEAR_REGEX_V1,
                        main_title=mov_main_title_modified,
                        rev_txt=mov_rev_txt_modified)
                elif re.search(YEAR_REGEX_V2 % mov_main_title_modified,
                               mov_rev_txt_modified, re.MULTILINE):
                    mov_referenced = does_release_year_match(
                        movie, YEAR_REGEX_V2,
                        main_title=mov_main_title_modified,
                        rev_txt=mov_rev_txt_modified)
                elif re.search(MOV_TITLE_V1.format(
                        mov_title=mov_main_title_modified),
                        mov_rev_txt_modified, re.MULTILINE) or re.search(
                    MOV_TITLE_V2.format(mov_title=mov_main_title_modified),
                        mov_rev_txt_modified, re.MULTILINE):
                    mov_referenced = True

                # update referenced mov object
                if mov_referenced and ReferencedMovie.objects.filter(
                        review=mov_rev_id).exists():
                    ref_mov = ReferencedMovie.objects.filter(
                        review=mov_rev_id).get()
                    self.stdout.write(
                        'UPDATING Referenced Movie object for movie: '
                        + str(movie) + ' and movie review: '
                        + str(MovieReview.objects.get(id=mov_rev_id)))
                    ref_mov.referenced_movie.add(movie)
                # create a new referenced movie object
                elif mov_referenced:
                    self.stdout.write(
                        'CREATING Referenced Movie object for movie: '
                        + str(movie) + ' and movie review: ' + str(
                            MovieReview.objects.get(id=mov_rev_id)))
                    ref_mov = ReferencedMovie()
                    ref_mov.review = MovieReview.objects.get(id=mov_rev_id)
                    ref_mov.save()
                    ref_mov.referenced_movie.add(movie)

        self.stdout.write(
            'Have finished adding entries for movies in the Referenced '
            'Movies DB table')
