from operator import attrgetter
import re
from random import randint
from django.db import models
import datetime
from ckeditor.fields import RichTextField
from django.core.urlresolvers import reverse
from django.db.models import Max, Min


def create_release_year_range():
    release_year_options = []
    release_start_year = 1895
    now = datetime.datetime.now()
    current_year = now.year
    year_option = release_start_year
    while year_option <= current_year:
        release_year_options.append((year_option, year_option))
        year_option += 1
    return release_year_options
# Create your models here.


class MovieMetadescriptors(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000, blank=True, default='')

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(MovieMetadescriptors):
    name = models.CharField(
        max_length=50, help_text='Enter the name of the genre')


class Subgenre(MovieMetadescriptors):
    name = models.CharField(max_length=50, help_text='Enter the name of the '
                                                     'subgenre')


class Microgenre(MovieMetadescriptors):
    name = models.CharField(max_length=50, help_text='Enter the name of the '
                                                     'microgenre')


class Keyword(MovieMetadescriptors):
    name = models.CharField(
        max_length=100, unique=True,
        help_text='Enter the keyword (or a keyword phrase)')


class WebsiteMetadescriptor(models.Model):
    website_name = models.CharField(max_length=50)
    contact_info = models.EmailField(
        max_length=50, help_text='Enter a contact email')
    mission_statement = RichTextField(blank=True)
    landing_page_title = models.CharField(max_length=50,
                                          default='The Horror Explosion')
    landing_page_description = models.CharField(
        max_length=155,
        default='Reviewing and analyzing post-1999 horror movies.')

    def __str__(self):
        return 'Website name: {website_name}\nContact Info: {' \
               'contact_info}'.format(
                        website_name=self.website_name,
                        contact_info=self.contact_info)


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    biography = RichTextField(max_length=1000, blank=True)
    photograph = models.ImageField(
        upload_to='people/', null=True, blank=True,
        help_text='Upload the person\'s photo')

    class Meta:
        abstract = True
        ordering = ['last_name']

    def __str__(self):
        if self.middle_name:
            return '{first_name} {middle_name} {last_name}'.format(
                first_name=self.first_name, middle_name=self.middle_name,
                last_name=self.last_name)
        else:
            return '{first_name} {last_name}'.format(
                first_name=self.first_name,
                last_name=self.last_name)


class Reviewer(Person):
    def __str__(self):
        return '{first_name}{last_name}'.format(first_name=self.first_name,
                                                last_name=self.last_name)


class MovieCreator(Person):
    pass


class Contributor(Person):
    pass


class Grade(models.Model):
    GRADE_CHOICES = (
        ('0.5', '0.5'),
        ('1.0', '1.0'),
        ('1.5', '1.5'),
        ('2.0', '2.0'),
        ('2.5', '2.5'),
        ('3.0', '3.0'),
        ('3.5', '3.5'),
        ('4.0', '4.0')
    )

    grade_numerical = models.CharField(
        max_length=3, choices=GRADE_CHOICES, help_text='Choose the motion '
                                                       'picture\'s grade')
    grade_description = models.CharField(
        max_length=50, help_text='Enter a short description of the grade')
    grade_depiction = models.ImageField(
        upload_to='images/', null=True,
        help_text='Upload the image corresponding to the grade')

    def __str__(self):
        return '{numerical_grade}'.format(numerical_grade=self.grade_numerical)

    class Meta:
        ordering = ['grade_numerical']


class PieceOfText(models.Model):
    review_author = models.ForeignKey(
        Reviewer, on_delete=models.SET_NULL, null=True,
        verbose_name='Text Author',
        help_text='Enter the name of the author')
    review_text = RichTextField(help_text='Enter the text',
                                verbose_name='Text')
    date_created = models.DateField(
        help_text='Enter the original date of the text creation')
    last_modified = models.DateField(auto_now=True)
    first_created = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        abstract = True


class Review(PieceOfText):
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True,
                              help_text='Choose the motion picture\'s grade')

    class Meta:
        abstract = True


class Article(PieceOfText):
    pass


class Country(models.Model):
    name = models.CharField(max_length=50, help_text='Enter the name of the ' \
                                                  'country')

    def __str__(self):
        return '{country_name}'.format(country_name=self.name)


class CreativeRole(models.Model):
    role_name = models.CharField(
        max_length=50, help_text='Enter the creative role that a person '
                                 'might have, e.g. Director, Editor, Writer, '
                                 'etc.')

    class Meta:
        ordering = ['role_name']

    def __str__(self):
        return '{role}'.format(role=self.role_name)


class MovieParticipation(models.Model):
    person = models.ForeignKey(MovieCreator, on_delete=models.CASCADE)
    creative_role = models.ForeignKey(CreativeRole, on_delete=models.CASCADE)

    def __str__(self):
        return '{creative_role}: {creator}'.format(
            creative_role=self.creative_role, creator=self.person)

    def return_creator_name(self):
        return self.person.__str__()

    class Meta:
        ordering = ['person']
        unique_together = ('person', 'creative_role')


class Title(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']


class MotionPicture(models.Model):
    release_year_options = []

    main_title = models.ForeignKey(
        Title, on_delete=models.SET_NULL, null=True, related_name='titles',
        help_text='Enter the motion picture\'s main title')
    title_for_sorting = models.CharField(
        max_length=250, null=True,
        help_text='Enter the title for sorting: Remove all stop words such '
                  'as "A", "An" and "The" and word all numbers')
    original_title = models.OneToOneField(
        Title, on_delete=models.SET_NULL, null=True, blank=True,
        help_text='Enter the motion picture\'s original title [OPTIONAL]')
    alternative_title = models.ManyToManyField(
        Title, blank=True, related_name='alternative_titles',
        help_text='Enter the motion picture\'s alternative_title(s) ['
                  'OPTIONAL]')
    year_of_release = models.IntegerField(
        choices=create_release_year_range(),
        help_text='Choose the motion picture\'s release year')
    duration = models.IntegerField(
        default=90, help_text='Enter the duration of the motion picture in '
                              'minutes')
    genre = models.ManyToManyField(
        Genre, help_text='Enter the motion picture\'s genre(s)')
    subgenre = models.ManyToManyField(
        Subgenre, blank=True, help_text='Enter the motion picture\'s '
                                                   'subgenre [OPTIONAL]')
    microgenre = models.ManyToManyField(
        Microgenre, blank=True, help_text='Enter the motion picture\'s '
                                                  'microgenre [OPTIONAL]')
    keyword = models.ManyToManyField(
        Keyword, help_text='Enter the keyword(s) that best describe the '
                           'motion picture')
    country_of_origin = models.ManyToManyField(
        Country, help_text='Enter the country of origin')
    poster = models.ImageField(
        upload_to='images/', null=True, blank=True,
        help_text='Upload the poster of the movie')
    poster_thumbnail = models.ImageField(
        upload_to='images/', null=True, blank=True,
        help_text='Upload the poster thumbnail')

    class Meta:
        abstract = True
        ordering = ['title_for_sorting']

    def __str__(self):
        return '{main_title} ({year_of_release})'.format(
            main_title=self.main_title, year_of_release=self.year_of_release)


class Movie(MotionPicture):
    movie_participation = models.ManyToManyField(
        MovieParticipation,
        help_text='Add the name of the movie creator and their role')
    is_direct_to_video = models.NullBooleanField(
        null=True, default=False, blank=True,
        help_text='Is the movie direct-to-video/DVD?')
    is_made_for_tv = models.NullBooleanField(
        null=True, default=False, blank=True,
        help_text='Is the movie made-for-TV?')
    first_created = models.DateField(auto_now_add=True, null=True, blank=True)
    human_readable_url = models.SlugField(
        help_text="Enter the 'slug',i.e., the human-readable "
                  "URL for the movie", unique=True, null=True)

    def get_absolute_url(self):
        return reverse('movie-detail', args=[str(self.id),
                                             str(self.human_readable_url)])

    def return_mov_participation_data(self, participation_type):
        participations = self.movie_participation.all()
        return [MovieParticipation for MovieParticipation in
                participations if str(MovieParticipation.creative_role) ==
                participation_type]


class MovieReview(Review):
    reviewed_movie = models.ForeignKey(
        Movie, null=True, help_text='Specify the reviewed movie')
    mov_review_page_description = models.CharField(
        max_length=155, default='Click on the link to see what we have to '
                                'say about this flick.')
    human_readable_url = models.SlugField(
        help_text="Enter the 'slug',i.e., the human-readable "
                  "URL for the movie review", unique=True, null=True)

    class Meta:
        ordering = ['reviewed_movie']

    def __str__(self):
        return '{movie_data} by {reviewer}'.format(
            movie_data=self.reviewed_movie, reviewer=self.review_author)

    def get_absolute_url(self):
        return reverse('moviereview-detail',
                       args=[str(self.id), str(self.human_readable_url)])


class ReferencedMovie(models.Model):
    referenced_movie = models.ManyToManyField(
        Movie, help_text='Add the referenced movie(s)')
    review = models.ForeignKey(
        MovieReview, null=True,
        help_text='Add the review where the movie was referenced')

    def __str__(self):
        return 'review {movie_review} references: {referenced_movie}'.format(
            movie_review=self.review,
            referenced_movie=', '.join(str(movie) for movie in \
                self.referenced_movie.all()))


class MovieInFranchise(models.Model):
    movie = models.ForeignKey(Movie, help_text='Enter the movie that\'s part '
                                               'of this franchise')
    position_in_franchise = models.IntegerField(
        default=1, help_text='Enter the movie\'s chronological position in '
                             'the '
                             'franchise as an integer, e.g. "1" for the '
                             'first '
                             'film in the franchise, "2" for the second '
                             'one, etc.')


class MovieFranchise(models.Model):
    franchise_name = models.CharField(
        max_length=50, help_text='Enter the name of the movie franchise')

    movies_in_franchise = models.ManyToManyField(
        MovieInFranchise, blank=True, help_text='List the movies '
                                                'that belong to the franchise')

    def __str__(self):
        return '{franchise_name}'.format(franchise_name=self.franchise_name)


class MovieRemake(models.Model):
    remade_movie = models.OneToOneField(
        Movie, related_name='remade_mov', help_text='Add the title of the '
                                                    'remade movie')
    remake = models.ManyToManyField(
        Movie, related_name='remake', help_text='Add the remake(s) of this '
                                                'movie')

    def __str__(self):
        return '{remade_mov} has been remade as: {remake}'.format(
            remade_mov=self.remade_movie,
            remake=', '.join(str(movie) for movie in
                             self.remake.all()))


def get_random_review(latest_review):
    qs = MovieReview.objects.all().exclude(pk=latest_review.pk)
    if not qs:
        return None
    max_pk = qs.aggregate(Max('pk'))['pk__max']
    min_pk = qs.aggregate(Min('pk'))['pk__min']
    counter = min_pk

    while counter <= max_pk:
        random_pk = randint(min_pk, max_pk)
        try:
            return qs.get(pk=random_pk)
        except qs.model.DoesNotExist:
            pass
        counter += 1
    # default return
    return qs.get(pk=min_pk)
