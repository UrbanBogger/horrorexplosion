import json
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


def mov_review_sd(mov_rev, db_object_absolute_url=''):
    review_author = ''
    if str(mov_rev.review_author) == 'M.S.':
        review_author = MS_REVIEW_AUTHOR
    elif str(mov_rev.review_author) == 'D.D.':
        review_author = DD_REVIEW_AUTHOR

    mov_directors = [str(mov_participation.person) for mov_participation in
                     return_mov_participation_data(
                         mov_rev.reviewed_movie, 'Director')]
    mov_cast = [str(mov_participation.person) for mov_participation in
                return_mov_participation_data(
                    mov_rev.reviewed_movie, 'Actor')]

    if mov_directors and len(mov_directors) == 1:
        dir_key = 'director'
        director = mov_directors[0]
    elif mov_directors and len(mov_directors) > 1:
        dir_key = 'directors'
        director = mov_directors

    country_of_origin = [str(country) for country in
                         mov_rev.reviewed_movie.country_of_origin.all()]
    if country_of_origin and len(country_of_origin) == 1:
        country_of_origin = country_of_origin[0]

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

