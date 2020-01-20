import re
import html
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.db.models import Q
from reviews.models import Movie, ReferencedMovie, MovieReview

RELEASE_YEAR_REGEX_PATTERN = r'.*\(\s?([0-9]{4})\s?\)'


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
                html_to_be_inspected = BeautifulSoup(mov_rev_txt_modified,
                                                     'html.parser')
                links = html_to_be_inspected.find_all('a')

                if ReferencedMovie.objects.filter(
                        Q(referenced_movie=movie) & Q(
                            review=mov_rev_id)).exists():
                    continue
                elif mov_main_title_modified in mov_rev_txt_modified:
                    for link in links:
                        print(link.attrs)
                        print(link.contents)
                        # check if link points to a IMDb Movie page
                        if 'title' in link.attrs['href']:
                            if any(mov_main_title_modified in link_txt for
                                   link_txt in link.contents) and any(
                                str(movie.year_of_release) in link_txt for
                                    link_txt in link.contents):
                                print('HAVE FOUND A MOVIE TITLE AND YEAR MATCH FOR:')
                                print(str(movie))
                                mov_referenced = True
                            elif any(mov_main_title_modified in link_txt for
                                   link_txt in link.contents):
                                print('HAVE ONLY FOUND THE MATCHING MOV TITLE FOR:')
                                print(str(movie))
                                # check if there any any release years present in the link
                                if not any(re.match(RELEASE_YEAR_REGEX_PATTERN, str(link_txt)) for link_txt in link.contents):
                                    print(
                                        'DID NOT FIND THE YEAR - ASSUMING '
                                        'IT\'S THE CORRECT MOV REFERENCE')
                                    mov_referenced = True
                                # check if there exists a year pattern
                                # anywhere in the link text
                                else:
                                    for link_txt in link.contents:
                                        # extract the release year
                                        if re.match(RELEASE_YEAR_REGEX_PATTERN, str(link_txt)):
                                            match = re.match(RELEASE_YEAR_REGEX_PATTERN, link_txt)
                                            year = match.group(1)
                                            print('HAVE FOUND THE FOLLOWING RELEASE YEAR: ' + str(year))
                                            if str(movie.year_of_release) == year:
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
