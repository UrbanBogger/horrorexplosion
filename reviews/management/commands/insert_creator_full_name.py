from django.core.management.base import BaseCommand
from reviews.models import MovieCreator


class Command(BaseCommand):
    help = 'Update the "Full Name" field in the Movie Creator table'

    def handle(self, *args, **options):
        self.stdout.write('Getting all creators that do not have the '
                          '"full name" field filled out.')
        creator_ids = MovieCreator.objects.filter(
            full_name__isnull=True).values_list('id', flat=True).order_by('id')

        if not creator_ids:
            self.stdout.write('Nothing to update. Exiting the script.')
        else:
            self.stdout.write('Beginning to update the database.')
            for creator_id in creator_ids:
                mov_creator = MovieCreator.objects.get(id=creator_id)
                creator_name = str(mov_creator)
                mov_creator.full_name = creator_name
                mov_creator.save()

            self.stdout.write('Have finished updating the database.')
