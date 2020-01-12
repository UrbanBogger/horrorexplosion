import re
import html
from django.core.management.base import BaseCommand
from django.db.models import Q
from reviews.models import Movie, ReferencedMovie, MovieReview


MOV_TITLE_V1 = r'<((?!.*wiki.*)a.*|em).*>{mov_title}<\/(a|em).*>'
MOV_TITLE_V2 = r'<!--.*{mov_title}\s*\([0-9]*\)-->'


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

            # check if there's another film with the same title
            mov_w_same_title = None
            if Movie.objects.exclude(id=movie_id).filter(
                    main_title=movie.main_title).exists():
                mov_w_same_title = Movie.objects.exclude(id=movie_id).filter(
                    main_title=movie.main_title).all()

            for mov_rev_id in all_mov_revs:
                mov_rev_txt_unescaped = html.unescape(MovieReview.objects.get(
                    id=mov_rev_id).review_text)
                mov_rev_txt_modified = mov_rev_txt_unescaped.replace(
                    '’', '').replace('\'', '')

                if ReferencedMovie.objects.filter(
                        Q(referenced_movie=movie) & Q(
                            review=mov_rev_id)).exists():
                    continue
                elif re.search(MOV_TITLE_V1.format(
                        mov_title=mov_main_title_modified),
                        mov_rev_txt_modified, re.MULTILINE) or re.search(
                    MOV_TITLE_V2.format(mov_title=mov_main_title_modified),
                        mov_rev_txt_modified, re.MULTILINE):
                        # update referenced mov object
                        if ReferencedMovie.objects.filter(
                                review=mov_rev_id).exists():
                            ref_mov = ReferencedMovie.objects.filter(
                                review=mov_rev_id).get()
                            if mov_w_same_title:
                                if re.search(r'\({release_year}\)'.format(
                                        release_year=str(
                                            movie.year_of_release)),
                                        mov_rev_txt_modified, re.MULTILINE):
                                    ref_mov.referenced_movie.add(movie)
                                else:
                                    for mov_st in mov_w_same_title:
                                        if re.search(
                                                r'\({release_year}\)'.format(
                                                    release_year=
                                                    str(mov_st.year_of_release)
                                                ), mov_rev_txt_modified,
                                                re.MULTILINE):
                                            ref_mov.referenced_movie.add(
                                                mov_st)
                            else:
                                self.stdout.write(
                                    'UPDATING Referenced Movie object for '
                                    'movie: '
                                    + str(movie) + ' and movie review: ' +
                                    str(MovieReview.objects.get(
                                        id=mov_rev_id)))
                                ref_mov.referenced_movie.add(movie)
                        # create a new referenced movie object
                        else:
                            self.stdout.write(
                                 'CREATING Referenced Movie object for movie: '
                                 + str(movie) + ' and movie review: ' + str(
                                     MovieReview.objects.get(id=mov_rev_id)))
                            ref_mov = ReferencedMovie()
                            ref_mov.review = MovieReview.objects.get(
                                id=mov_rev_id)
                            ref_mov.save()
                            if mov_w_same_title:
                                if re.search(r'\({release_year}\)'.format(
                                        release_year=str(
                                            movie.year_of_release)),
                                        mov_rev_txt_modified, re.MULTILINE):
                                    ref_mov.referenced_movie.add(movie)
                                else:
                                    for mov_st in mov_w_same_title:
                                        if re.search(
                                                r'\({release_year}\)'.format(
                                                    release_year=
                                                    str(mov_st.year_of_release)
                                                ), mov_rev_txt_modified,
                                                re.MULTILINE):
                                            ref_mov.referenced_movie.add(
                                                mov_st)
                            else:
                                ref_mov.referenced_movie.add(movie)

        self.stdout.write(
            'Have finished adding entries for movies in the Referenced '
            'Movies DB table')
