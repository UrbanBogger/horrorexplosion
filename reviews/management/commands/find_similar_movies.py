import math
from operator import itemgetter
from django.core.management.base import BaseCommand
from django.db.models import Q
from reviews.models import Movie, MovieSeries, MovieRemake, SimilarMovie, \
    MovSeriesEntry

# key: bonus points as exponents of number 2; value: increase in the overall
#  similarity percentage (as a prime number series - except for 1)
BONUS_POINT_SCALE = {1: 1, 2: 2, 3: 3, 4: 5, 5: 7, 6: 11, 7: 13, 8: 17,
                     9: 19, 10: 23, 11: 29, 12: 31, 13: 37, 14: 41, 15: 43,
                     16: 47, 17: 47, 18: 47, 19: 47, 20: 47, 21: 48, 22: 49}
OVERALL_SIMILARITY_PERCENTAGE_MAX = 100


def determine_similarity_level(similarity_exponent):
    similarity_level = ''
    alert_type = ''

    if 0 <= similarity_exponent <= 20:
        similarity_level = 'VERY LOW'
        alert_type = 'alert-dark'
    elif 21 <= similarity_exponent <= 40:
        similarity_level = 'LOW'
        alert_type = 'alert-warning'
    elif 41 <= similarity_exponent <= 60:
        similarity_level = 'MEDIUM'
        alert_type = 'alert-info'
    elif 61 <= similarity_exponent <= 80:
        similarity_level = 'HIGH'
        alert_type = 'alert-success'
    elif similarity_exponent >= 81:
        similarity_level = 'VERY HIGH'
        alert_type = 'alert-danger'

    return similarity_level, alert_type


def calculate_bonus_similarity_pts(similar_mov_list, movie):
    keywords_and_points = [
        ('anthology film', 4), ('atmospheric', 2), ('bizarre', 2),
        ('Camp Crystal Lake', 2), ('Charles Band related', 3),
        ('Christmas season', 3), ('Creeper [the]', 3),
        ('found footage narrative', 3), ('Graboid(s)', 3),
        ('H. P. Lovecraft related', 3), ('Jason Voorhees', 3),
        ('Krampus', 3), ('Leatherface', 3),
        ('literary adaptation', 2), ('lovecraftian', 3),
        ('low budget (>$100,000 but <=$1,000,000)', 3),
        ('micro budget (<=$100,000)', 3), ('Netflix Original Film', 2),
        ('Pamela Voorhees', 2), ('Pennywise the Clown', 3),
        ('Platinum Dunes', 2), ('Polonia brothers', 3),
        ('regional horror film', 3), ('remake [a]', 2),
        ('Santa Claus', 2), ('shot on video (SOV)', 2), ('Splat Pack', 3),
        ('splatter', 2), ('Stephen King related', 3),
        ('Sterling Entertainment production', 3), ('stylized', 2),
        ('Sub Rosa', 3), ('surreal', 2), ('toilet humour', 3),
        ('Troma-distributed', 3), ('Troma production', 3),
        ('underground horror', 4), ('Victor Crowley', 3)
    ]
    mov_directors = [mov_participation.person for mov_participation in
                     movie.movie_participation.filter(
                         creative_role__role_name='Director')]
    mov_series = None
    mov_franchises = None
    mov_similarity_list = []

    # check if mov  is part of a franchise
    if MovSeriesEntry.objects.filter(movie_in_series=movie).exists():
        mov_franchises = [mov_franchise for mov_series_entry in
                          MovSeriesEntry.objects.filter(movie_in_series=movie)
                          for mov_franchise in
                          mov_series_entry.franchise_association.all()]

    if MovieSeries.objects.filter(mov_series__movie_in_series=movie).exists():
        mov_series = MovieSeries.objects.filter(
            mov_series__movie_in_series=movie)

    for mov_tuple in similar_mov_list:
        mov_tuple_as_list = list(mov_tuple)
        bonus_similarity_exponent = 0
        bonus_similarity_points = 0
        # do the movies have the same country of origin (exact matches only
        # for now)
        if set(list(mov_tuple_as_list[1].country_of_origin.all())) == set(list(
                movie.country_of_origin.all())):
            bonus_similarity_exponent += 1
        # do the movies have the same director (exact matches only for now)
        if set([mov_participation.person for mov_participation in
                         mov_tuple_as_list[1].movie_participation.filter(
                             creative_role__role_name='Director')]) == set(
                mov_directors):
            bonus_similarity_exponent += 2

        if movie.is_direct_to_video and mov_tuple_as_list[1].is_direct_to_video:
            bonus_similarity_exponent += 2

        if movie.is_made_for_tv and mov_tuple_as_list[1].is_made_for_tv:
            bonus_similarity_exponent += 2
        # are we dealing with a remake?
        if MovieRemake.objects.filter(Q(remade_movie=movie) & Q(
                remake=mov_tuple_as_list[1])).exists() or \
                MovieRemake.objects.filter(
                    Q(remade_movie=mov_tuple_as_list[1]) &
                            Q(remake=movie)).exists():
            bonus_similarity_exponent += 3
        # do the 2 movies belong to the same movie series?
        if mov_series:
            if mov_series.filter(
                    mov_series__movie_in_series=mov_tuple_as_list[1]).exists():
                bonus_similarity_exponent += 3
        # do the 2 movies belong to the same Franchise or Series
        if mov_franchises:
            for mov_franchise in mov_franchises:
                if mov_franchise.movseriesentry_set.filter(
                        movie_in_series=mov_tuple_as_list[1]).exists():
                            bonus_similarity_exponent += 3
        # check for special keywords last
        for keyword_point_tuple in keywords_and_points:
            if movie.keyword.filter(name=keyword_point_tuple[0]).exists() and \
                    mov_tuple_as_list[1].keyword.filter(
                        name=keyword_point_tuple[0]).exists():
                bonus_similarity_exponent += keyword_point_tuple[1]

        # increase the overall similarity based on bonus similarity points
        if bonus_similarity_exponent != 0:
            mov_similarity_tuple_as_list = list(mov_tuple_as_list[0])
            mov_similarity_tuple_as_list[0] += BONUS_POINT_SCALE[
                bonus_similarity_exponent]
            mov_tuple_as_list[0] = mov_similarity_tuple_as_list
            if mov_similarity_tuple_as_list[0] >= 100:
                mov_similarity_tuple_as_list[0] = \
                    OVERALL_SIMILARITY_PERCENTAGE_MAX

        bonus_similarity_points = int(math.pow(2, bonus_similarity_exponent))
        mov_similarity_list.append(
            (tuple(mov_tuple_as_list[0]), mov_tuple_as_list[1],
                bonus_similarity_points))
    # sort similar movies based on overall percentage and bonus points
    return sorted(mov_similarity_list, key=itemgetter(0, 2), reverse=True)


def get_similar_movies(movie, all_movies):
    keywords = set([kw.name for kw in movie.keyword.all()])
    all_metagenre_tags = set(
        [genre.name for genre in movie.genre.all()] +
        [sg.name for sg in movie.subgenre.all()] +
        [mg.name for mg in movie.microgenre.all()])
    mov_similarity_list = []

    for current_mov_id in all_movies:
        current_mov = Movie.objects.get(id=current_mov_id)
        percentage_of_keyword_matches = 0
        percentage_of_metagenre_matches = 0
        overall_similarity_percentage = 0

        keywords_to_compare = set([kw.name for kw in
                                   current_mov.keyword.all()])

        if list(keywords & keywords_to_compare):
            percentage_of_keyword_matches = round(
                len(list(keywords & keywords_to_compare)) /
                float(len(keywords | keywords_to_compare)), 2) * 100

        metagenre_tags_to_compare = set(
            [genre.name for genre in current_mov.genre.all()]
            + [sg.name for sg in current_mov.subgenre.all()]
            + [mg.name for mg in current_mov.microgenre.all()])

        if list(all_metagenre_tags & metagenre_tags_to_compare):
            percentage_of_metagenre_matches = round(
                len(list(all_metagenre_tags & metagenre_tags_to_compare)) /
                float(len(all_metagenre_tags | metagenre_tags_to_compare)
                      ), 2) * 100

        overall_similarity_percentage = int(
            round((percentage_of_keyword_matches +
                   percentage_of_metagenre_matches) / 2.0, 0))

        mov_similarity_list.append(((overall_similarity_percentage,
                                     int(percentage_of_keyword_matches),
                                     int(percentage_of_metagenre_matches)),
                                    current_mov))

    if len(mov_similarity_list) >= 15:
        similar_movies = calculate_bonus_similarity_pts(
            sorted(mov_similarity_list, key=itemgetter(0), reverse=True)[:15],
            movie)
    else:
        similar_movies = calculate_bonus_similarity_pts(
            sorted(mov_similarity_list, key=itemgetter(0), reverse=True),
            movie)

    mov_similarity_list = []
    for similar_movie_tuple in similar_movies:
        similarity_level, alert_type = determine_similarity_level(
            similar_movie_tuple[0][0])
        mov_similarity_list.append(
            {'similarity_percentages': similar_movie_tuple[0],
             'similarity_level': similarity_level,
             'compared_mov': movie,
             'similar_mov': similar_movie_tuple[1],
             'alert_type': alert_type,
             'bonus_similarity_points': similar_movie_tuple[2]})

    if len(mov_similarity_list) < 4:
        return mov_similarity_list

    return mov_similarity_list[:4]


class Command(BaseCommand):
    help = 'Finds similar movies for each movie in the database and stores ' \
           'the results in the SimilarMovies DB table'

    def handle(self, *args, **options):
        # delete all rows in the 'SimilarMovie' table
        self.stdout.write('Deleting all rows in the SimilarMovies table')
        all_movies = Movie.objects.values_list('id', flat=True).order_by('id')
        self.stdout.write('Beginning to calculate movie similarity for each '
                          'movie in the DB')

        for movie_id in all_movies:
            movie = Movie.objects.get(id=movie_id)
            all_other_movies = Movie.objects.values_list(
                'id', flat=True).exclude(pk=movie.pk).order_by('id')
            similar_movies = get_similar_movies(movie, all_other_movies)
            # delete all rows in the 'SimilarMovie' table for the current movie
            SimilarMovie.objects.filter(compared_mov=movie).delete()
            # repopulate the table rows for the movie
            for similar_movie_dict in similar_movies:
                similar_mov = SimilarMovie()
                similar_mov.compared_mov = similar_movie_dict['compared_mov']
                similar_mov.similar_mov = similar_movie_dict['similar_mov']
                similar_mov.overall_similarity_percentage = similar_movie_dict[
                    'similarity_percentages'][0]
                similar_mov.keyword_similarity_percentage = similar_movie_dict[
                    'similarity_percentages'][1]
                similar_mov.metagenre_similarity_percentage = \
                    similar_movie_dict[
                        'similarity_percentages'][2]
                similar_mov.bonus_similarity_points = similar_movie_dict[
                    'bonus_similarity_points']
                similar_mov.similarity_category = similar_movie_dict[
                    'similarity_level']
                similar_mov.alert_type = similar_movie_dict['alert_type']
                similar_mov.save()
        self.stdout.write(
            'Have finished adding entries for all movies in the DB')
