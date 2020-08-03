from .models import return_mov_participation_data

MS_REVIEW_AUTHOR = 'Mitch Sokolov'
DD_REVIEW_AUTHOR = 'Dave Dukowski'
ORGANIZATION_NAME = 'The Horror Explosion'
ORGANIZATION_HOME_URL = 'http://www.horrorexplosion.com/'
CONTRIBUTORS_URL = 'http://www.horrorexplosion.com/reviews/contributors/'
CONTEXT = 'https://schema.org'
CONTEXT_KEY = '@context'
TYPE_KEY = '@type'
REVIEW_TYPE = 'Review'
PERSON_TYPE = 'Person'
ORGANISATION_TYPE = 'Organization'
MOVIE_TYPE = 'Movie'
TV_SERIES_TYPE = 'TVSeries'
TV_SEASON_TYPE = 'TVSeason'
TV_EPISODE_TYPE = 'TVEpisode'


def get_review_author(review):
    review_author = ''

    if str(review.review_author) == 'M.S.':
        review_author = MS_REVIEW_AUTHOR
    elif str(review.review_author) == 'D.D.':
        review_author = DD_REVIEW_AUTHOR

    return review_author


def get_director_key(directors):
    dir_key = None
    director = None

    if directors and len(directors) == 1:
        dir_key = 'director'
        director = directors[0]
    elif directors and len(directors) > 1:
        dir_key = 'directors'
        director = directors

    return dir_key, director


def mov_review_sd(mov_rev, db_object_absolute_url=''):
    review_author = get_review_author(mov_rev)

    mov_directors = [str(mov_participation.person) for mov_participation in
                     return_mov_participation_data(
                         mov_rev.reviewed_movie, 'Director')]
    mov_cast = [str(mov_participation.person) for mov_participation in
                return_mov_participation_data(
                    mov_rev.reviewed_movie, 'Actor')]

    dir_key, director = get_director_key(mov_directors)

    country_of_origin = [str(country) for country in
                         mov_rev.reviewed_movie.country_of_origin.all()]
    if country_of_origin and len(country_of_origin) == 1:
        country_of_origin = country_of_origin[0]

    if not (mov_cast and director and country_of_origin):
        return None

    structured_data = {
        CONTEXT_KEY: CONTEXT,
        TYPE_KEY: REVIEW_TYPE,
        'author': {TYPE_KEY: PERSON_TYPE,
                   'name': review_author,
                   'sameAs': CONTRIBUTORS_URL},
        'url': db_object_absolute_url,
        'datePublished': mov_rev.first_created.isoformat(),
        'publisher': {TYPE_KEY: ORGANISATION_TYPE,
                      'name': ORGANIZATION_NAME,
                      'sameAs': ORGANIZATION_HOME_URL},
        'description': mov_rev.mov_review_page_description,
        'inLanguage': 'en',
        'itemReviewed': {TYPE_KEY: MOVIE_TYPE,
                         'name': str(mov_rev.reviewed_movie.main_title),
                         'sameAs': mov_rev.reviewed_movie.imdb_link,
                         'image': mov_rev.reviewed_movie.poster.url,
                         dir_key: director,
                         'actors': mov_cast,
                         'countryOfOrigin': country_of_origin,
                         'dateCreated': str(
                             mov_rev.reviewed_movie.year_of_release),
                         },
        'reviewRating': {TYPE_KEY: 'Rating',
                         'worstRating': 0.5,
                         'bestRating': 4.0,
                         'ratingValue': float(mov_rev.grade.grade_numerical)},
        'reviewBody': mov_rev.review_snippet
    }
    return structured_data


def mov_sd(movie):
    mov_directors = [str(mov_participation.person) for mov_participation in
                     return_mov_participation_data(movie, 'Director')]
    mov_cast = [str(mov_participation.person) for mov_participation in
                return_mov_participation_data(movie, 'Actor')]

    dir_key, director = get_director_key(mov_directors)

    country_of_origin = [str(country) for country in
                         movie.country_of_origin.all()]

    if country_of_origin and len(country_of_origin) == 1:
        country_of_origin = country_of_origin[0]

    if not (mov_cast and director and country_of_origin):
        return None

    structured_data = {
        CONTEXT_KEY: CONTEXT,
        TYPE_KEY: MOVIE_TYPE,
        'name': str(movie.main_title),
        'sameAs': movie.imdb_link,
        'image': movie.poster.url,
        dir_key: director,
        'actors': mov_cast,
        'countryOfOrigin': country_of_origin,
        'dateCreated': str(movie.year_of_release)
    }
    return structured_data


def tv_episode_rev_sd(tv_episode_rev, db_object_absolute_url=''):
    grade = None
    review_author = get_review_author(tv_episode_rev)
    print('MOV PARTICIPATIONS: ' + str(return_mov_participation_data(
        tv_episode_rev.reviewed_tv_episode, 'Director')))
    episode_directors = [str(mov_participation.person) for mov_participation in
                         return_mov_participation_data(
                         tv_episode_rev.reviewed_tv_episode, 'Director')]
    episode_cast = [str(mov_participation.person) for mov_participation in
                    return_mov_participation_data(
                         tv_episode_rev.reviewed_tv_episode, 'Actor')]
    print('DIRECTORS: ' + str(episode_directors))
    dir_key, director = get_director_key(episode_directors)

    image = None
    if tv_episode_rev.reviewed_tv_episode.poster:
        image = tv_episode_rev.reviewed_tv_episode.poster.url
    else:
        image = tv_episode_rev.reviewed_tv_episode.tv_season.tv_series.poster.\
            url

    country_of_origin = [
        str(country) for country in
        tv_episode_rev.reviewed_tv_episode.tv_season.country_of_origin.all()]
    if country_of_origin and len(country_of_origin) == 1:
        country_of_origin = country_of_origin[0]

    if not (episode_cast and director and image and country_of_origin):
        return None

    if tv_episode_rev.grade:
        grade = float(tv_episode_rev.grade.grade_numerical)
    elif tv_episode_rev.tvepisodesegmentreview_set.all().exists():
        grades = [float(tv_ep_rev_seg.grade.grade_numerical)
                  for tv_ep_rev_seg in
                  tv_episode_rev.tvepisodesegmentreview_set.all()]
        grade = round(sum(grades)/len(grades) * 2.0 / 2.0)

    structured_data = {
        CONTEXT_KEY: CONTEXT,
        TYPE_KEY: REVIEW_TYPE,
        'author': {TYPE_KEY: PERSON_TYPE,
                   'name': review_author,
                   'sameAs': CONTRIBUTORS_URL},
        'url': db_object_absolute_url,
        'datePublished': tv_episode_rev.first_created.isoformat(),
        'publisher': {TYPE_KEY: ORGANISATION_TYPE,
                      'name': ORGANIZATION_NAME,
                      'sameAs': ORGANIZATION_HOME_URL},
        'description': tv_episode_rev.mov_review_page_description,
        'inLanguage': 'en',
        'itemReviewed': {TYPE_KEY: TV_SERIES_TYPE,
                         'name': str(tv_episode_rev.reviewed_tv_episode.
                                     tv_season.tv_series.main_title),
                         'sameAs': tv_episode_rev.reviewed_tv_episode.
                         tv_season.tv_series.imdb_link,
                         'containsSeason': {
                             'datePublished': tv_episode_rev.
                             reviewed_tv_episode.tv_season.year_of_release,
                             'episode': {
                                TYPE_KEY: TV_EPISODE_TYPE,
                                'episodeNumber': str(
                                    tv_episode_rev.reviewed_tv_episode.
                                    episode_number),
                                'name': tv_episode_rev.reviewed_tv_episode.
                                episode_title,
                                'sameAs': tv_episode_rev.reviewed_tv_episode.
                                imdb_link,
                                'image': str(image),
                                dir_key: director,
                                'actors': episode_cast,
                                'countryOfOrigin': country_of_origin
                             },
                             'name': tv_episode_rev.reviewed_tv_episode.
                             tv_season.season_title
                             }
                         },
        'reviewRating': {TYPE_KEY: 'Rating',
                         'worstRating': 0.5,
                         'bestRating': 4.0,
                         'ratingValue': grade},
        'reviewBody': tv_episode_rev.review_snippet
    }
    return structured_data
