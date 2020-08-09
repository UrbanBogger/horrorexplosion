from django.core.management.base import BaseCommand
from reviews.models import MovieCreator, Movie, TelevisionSeries, \
    TelevisionSeason, TelevisionEpisode

SPECIAL_CHARS_DICT = {
    '\'': '', '’': '', '.': '', '-': ' ',
    ':': '', '&': '', '!': '', 'â': 'a',
    'à': 'a', 'á': 'a', 'å': 'a', 'ä': 'a', 'æ': 'ae',
    'ç': 'c', 'è': 'e', 'é': 'e', 'ë': 'e',
    'ï': 'i', 'í': 'i', 'ñ': 'n',
    'ô': 'o', 'ó': 'o', 'ø': 'o', 'ö': 'o',
    'ú': 'u', 'û': 'u', 'ý': 'y'}


class Command(BaseCommand):
    help = 'Add special character free entries to database models that are ' \
           'part of the search'
    special_char_list = list(SPECIAL_CHARS_DICT.keys())

    def handle(self, *args, **options):
        self.stdout.write('Removing special characters from searchable models')

        creator_ids = MovieCreator.objects.filter(
            full_name__isnull=False).values_list('id', flat=True).order_by(
            'id')

        if not creator_ids:
            self.stdout.write('No creators to update.')
        else:
            self.stdout.write('Updating creator entries.')

            for creator_id in creator_ids:
                full_name = str(MovieCreator.objects.get(
                    id=creator_id).full_name)
                full_name_wo_special_chars = self.replace_special_characters(
                    full_name)

                mov_creator = MovieCreator.objects.get(id=creator_id)
                mov_creator.full_name_wo_special_chars = \
                    full_name_wo_special_chars
                mov_creator.save()

        movie_ids = Movie.objects.values_list('id', flat=True).order_by('id')

        if not creator_ids:
            self.stdout.write('No movies to update.')
        else:
            self.stdout.write('Updating movie entries.')

        for mov_id in movie_ids:
            main_title = str(Movie.objects.get(id=mov_id).main_title)
            main_title_wo_special_chars = self.replace_special_characters(
                main_title)
            og_title = str(Movie.objects.get(id=mov_id).original_title)
            og_title_wo_special_chars = self.replace_special_characters(
                og_title)
            alt_titles = Movie.objects.get(id=mov_id).alternative_title.all()
            alt_titles_wo_spec_chars = ' '.join(
                [self.replace_special_characters(str(alt_title)) for alt_title
                 in alt_titles])

            movie = Movie.objects.get(id=mov_id)
            movie.main_title_wo_special_chars = main_title_wo_special_chars
            movie.og_title_wo_special_chars = og_title_wo_special_chars
            movie.alt_title_wo_special_chars = alt_titles_wo_spec_chars
            movie.save()

        tv_series_ids = TelevisionSeries.objects.values_list(
            'id', flat=True).order_by('id')

        if not tv_series_ids:
            self.stdout.write('No TV Series to update.')
        else:
            self.stdout.write('Updating TV Series entries.')

        for tv_series_id in tv_series_ids:
            main_title = str(TelevisionSeries.objects.get(
                id=tv_series_id).main_title)
            main_title_wo_special_chars = self.replace_special_characters(
                main_title)
            og_title = str(TelevisionSeries.objects.get(
                id=tv_series_id).original_title)
            og_title_wo_special_chars = self.replace_special_characters(
                og_title)
            alt_titles = TelevisionSeries.objects.get(
                id=tv_series_id).alternative_title.all()
            alt_titles_wo_spec_chars = ' '.join(
                [self.replace_special_characters(str(alt_title)) for alt_title
                 in alt_titles])

            tv_series = TelevisionSeries.objects.get(id=tv_series_id)
            tv_series.main_title_wo_special_chars = main_title_wo_special_chars
            tv_series.og_title_wo_special_chars = og_title_wo_special_chars
            tv_series.alt_title_wo_special_chars = alt_titles_wo_spec_chars
            tv_series.save()

        tv_season_ids = TelevisionSeason.objects.values_list(
            'id', flat=True).order_by('id')

        if not tv_season_ids:
            self.stdout.write('No TV Seasons to update.')
        else:
            self.stdout.write('Updating TV Season entries.')

        for tv_season_id in tv_season_ids:
            season_title = str(TelevisionSeason.objects.get(
                id=tv_season_id).season_title)
            season_title_wo_special_chars = self.replace_special_characters(
                season_title)

            tv_season = TelevisionSeason.objects.get(id=tv_season_id)
            tv_season.season_title_wo_special_chars = \
                season_title_wo_special_chars
            tv_season.save()

        tv_ep_ids = TelevisionEpisode.objects.values_list(
            'id', flat=True).order_by('id')

        if not tv_ep_ids:
            self.stdout.write('No TV Episodes to update.')
        else:
            self.stdout.write('Updating TV Episode entries.')

        for tv_ep_id in tv_ep_ids:
            ep_title = str(TelevisionEpisode.objects.get(
                id=tv_ep_id).episode_title)
            ep_title_wo_special_chars = self.replace_special_characters(
                ep_title)

            tv_episode = TelevisionEpisode.objects.get(id=tv_ep_id)
            tv_episode.ep_title_wo_special_chars = ep_title_wo_special_chars
            tv_episode.save()

    def replace_special_characters(self, search_term):
        search_term = search_term.lower()

        for character in search_term:
            if character in self.special_char_list:
                search_term = search_term.replace(
                    character, SPECIAL_CHARS_DICT[character])

        return search_term
