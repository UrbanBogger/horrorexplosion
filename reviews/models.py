import random
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


def return_mov_participation_data(motion_pic_obj, participation_type):
    participations = motion_pic_obj.movie_participation.all()
    return [MovieParticipation for MovieParticipation in participations if
            str(MovieParticipation.creative_role) == participation_type]
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
    last_name = models.CharField(max_length=50, blank=True)
    biography = RichTextField(max_length=1000, blank=True)
    photograph = models.ImageField(
        upload_to='people/', null=True, blank=True,
        help_text='Upload the person\'s photo')

    class Meta:
        abstract = True
        ordering = ['last_name']
        unique_together = ('first_name', 'middle_name', 'last_name')

    def __str__(self):
        if self.middle_name:
            return '{first_name} {middle_name} {last_name}'.format(
                first_name=self.first_name, middle_name=self.middle_name,
                last_name=self.last_name)
        elif not self.last_name:
            return '{first_name}'.format(first_name=self.first_name)
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
        upload_to='grade_depictions/', null=True,
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

    class Meta:
        ordering = ['name']

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
    position_in_credits = models.IntegerField(
        default=1, help_text='Enter the position you want this creator to '
                             'appear in the list, e.g. "1" means the first '
                             'position in the list, "2" the second, etc.')

    def __str__(self):
        return '{position}: {creative_role}: {creator}'.format(
            position=self.position_in_credits,
            creative_role=self.creative_role, creator=self.person)

    def return_creator_name(self):
        return self.person.__str__()

    class Meta:
        ordering = ['position_in_credits', 'person']
        unique_together = ('person', 'creative_role', 'position_in_credits')


class Title(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']


class MovieFranchise(models.Model):
    franchise_name = models.CharField(
        max_length=50, help_text='Enter the name of the movie franchise')

    def __str__(self):
        return '{franchise_name}'.format(franchise_name=self.franchise_name)


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
        upload_to='movie_posters/', null=True, blank=True,
        help_text='Upload the poster of the movie')
    poster_thumbnail = models.ImageField(
        upload_to='movie_posters/thumbnails/', null=True, blank=True,
        help_text='Upload the poster thumbnail')
    first_created = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['title_for_sorting']

    def __str__(self):
        return '{main_title} ({year_of_release})'.format(
            main_title=self.main_title, year_of_release=self.year_of_release)


class Movie(MotionPicture):
    movie_participation = models.ManyToManyField(
        MovieParticipation, help_text='Add the name of the movie creator and '
                                                           'their role')
    is_direct_to_video = models.NullBooleanField(
        null=True, default=False, blank=True,
        help_text='Is the movie direct-to-video/DVD?')
    is_made_for_tv = models.NullBooleanField(
        null=True, default=False, blank=True,
        help_text='Is the movie made-for-TV?')
    human_readable_url = models.SlugField(
        help_text="Enter the 'slug',i.e., the human-readable "
                  "URL for the movie", unique=True, null=True)
    imdb_link = models.CharField(max_length=250, null=True, blank=True,
                                 help_text='Enter the link to the IMDb')

    def get_absolute_url(self):
        return reverse('movie-detail', args=[str(self.id),
                                             str(self.human_readable_url)])

    def get_meta_string(self):
        title = 'Main Title:{title}|'.format(title=str(self.main_title.title))
        year = 'Year:{year}|'.format(year=str(self.year_of_release))
        length = 'Length:{length} min.|'.format(length=str(self.duration))
        country = 'Country:{country}|'.format(
            country='/'.join([country.name for country in
                              self.country_of_origin.all()]))
        genre = 'Genre:{genre}|'.format(genre=','.join([genre.name for genre in
                                                       self.genre.all()]))
        og_title = ''
        if self.original_title:
            og_title = 'OG Title:{og_title}|'.format(og_title=str(
                self.original_title.title))
        alt_title = ''
        if self.alternative_title.all():
            alt_title = 'Alt Title:{alt_title}|'.format(alt_title=','.join(
                [alt_title.title for alt_title in
                 self.alternative_title.all()]))
        subgenre = ''
        if self.subgenre.all():
            subgenre = 'Subgenre:{subgenre}|'.format(
                subgenre=','.join([subgenre.name for subgenre in
                                   self.subgenre.all()]))
        microgenre = ''
        if self.microgenre.all():
            microgenre = 'Microgenre:{microgenre}|'.format(
                microgenre=','.join([microgenre.name for microgenre in
                                   self.microgenre.all()]))
        if self.moviereview_set.all():
             review = 'Our Review:Exists|'
        else:
            review = 'Our Review:None Yet|'
        director = 'Dir.:{director}'.format(director=','.join(
            [str(mov_participation.person) for mov_participation in
             self.movie_participation.filter(
                 creative_role__role_name='Director')]))
        return f'{title}{og_title}{alt_title}{year}{length}{country}{genre}' \
            f'{subgenre}{microgenre}{review}{director}'


class MovieReview(Review):
    reviewed_movie = models.ForeignKey(
        Movie, null=True, help_text='Specify the reviewed movie')
    mov_review_page_description = models.CharField(
        max_length=155, default='Click on the link to see what we have to '
                                'say about this flick.')
    human_readable_url = models.SlugField(
        help_text="Enter the 'slug',i.e., the human-readable "
                  "URL for the movie review", unique=True, null=True)
    review_snippet = models.TextField(
        unique=True, null=True, max_length=800,
        help_text='Enter the Review snippet for Google Structured Data '
                  '[OPTIONAL]')

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
        MovieReview, null=True, help_text='Add the review where the movie '
                                     'was referenced')

    def __str__(self):
        return 'review {movie_review} references: {referenced_movie}'.format(
            movie_review=self.review,
            referenced_movie=', '.join(str(movie) for movie in \
                self.referenced_movie.all()))


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


class MovieInMovSeries(models.Model):
    movie_in_series = models.ForeignKey(
        Movie, help_text='Enter the movie that\'s part of this series')
    position_in_series = models.IntegerField(
        default=1, help_text='Enter the movie\'s chronological position in '
                             'the '
                             'series as an integer, e.g. "1" for the '
                             'first '
                             'film in the franchise, "2" for the second '
                             'one, etc.')

    class Meta:
        ordering = ['position_in_series']

    def __str__(self):
        return '{position_in_series}: {movie_in_series}'.format(
            position_in_series=self.position_in_series,
            movie_in_series=self.movie_in_series)


class MovieSeries(models.Model):
    mov_series = models.ManyToManyField(
        MovieInMovSeries, help_text='Enter the movie and its position in the '
                                    'movie series')
    franchise_association = models.ForeignKey(
        MovieFranchise, on_delete=models.SET_NULL, null=True, blank=True,
        help_text='Choose the franchise this movie might belong to[OPTIONAL]')

    def __str__(self):
        return 'Movies in this series: {movie_list}'.format(
            movie_list=', '.join(str(mov_in_series) for mov_in_series in
                                 self.mov_series.all()))


class SimilarMovie(models.Model):
    compared_mov = models.ForeignKey(Movie, on_delete=models.CASCADE,
                                     related_name='mov_being_compared')
    similar_mov = models.ForeignKey(Movie, on_delete=models.CASCADE,
                                    related_name='similar_mov')
    overall_similarity_percentage = models.IntegerField()
    metagenre_similarity_percentage = models.IntegerField()
    keyword_similarity_percentage = models.IntegerField()
    bonus_similarity_points = models.IntegerField()
    similarity_category = models.CharField(max_length=250)
    alert_type = models.CharField(max_length=250)

    def __str__(self):
        return '{compared_mov} is similar to {similar_mov}'.format(
            compared_mov=self.compared_mov, similar_mov=self.similar_mov)


class TelevisionSeries(models.Model):
    SERIES_TYPES = (
        ('Mini-Series', 'TV Mini-Series'),
        ('Anthology', 'Anthology (Episodic) TV Series'),
        ('Serial', 'Serial TV Series'),)

    main_title = models.ForeignKey(Title, on_delete=models.SET_NULL,
                                   related_name='tv_series_main_title_set',
                                   null=True, help_text='Enter the TV '
                                                        'serie\'s main title')
    title_for_sorting = models.CharField(
        max_length=250, null=True,
        help_text='Enter the title for sorting: Remove all stop words such '
                  'as "A", "An" and "The" and word all numbers')
    original_title = models.OneToOneField(
        Title, on_delete=models.SET_NULL, null=True, blank=True,
        help_text='Enter the TV serie\'s original title [OPTIONAL]')
    alternative_title = models.ManyToManyField(
        Title, blank=True, related_name='tv_series_alternative_title_set',
        help_text='Enter the TV serie\'s alternative_title(s) ['
                  'OPTIONAL]')
    is_still_running = models.NullBooleanField(
        null=True, default=False, help_text='Is TV series still ongoing?')
    poster = models.ImageField(
        upload_to='tv_series_posters/', null=True,
        help_text='Upload the top-level poster for the TV series if '
                  'applicable [OPTIONAL]')
    poster_thumbnail = models.ImageField(
        upload_to='tv_series_posters/thumbnails/', null=True,
        help_text='Upload the top-level poster thumbnail for the TV series '
                  'if applicable [OPTIONAL]')
    description = RichTextField(blank=True, help_text='Provide background '
                                                      'info on the TV series '
                                                      '[OPTIONAL]')
    tv_series_type = models.CharField(max_length=25, choices=SERIES_TYPES)
    first_created = models.DateField(auto_now_add=True, null=True, blank=True)
    human_readable_url = models.SlugField(
        help_text="Enter the 'slug',i.e., the human-readable "
                  "URL for the TV series", unique=True, null=True)

    @property
    def get_season_reviews(self):
        return [tv_season_review for tv_season in
                self.televisionseason_set.all() for tv_season_review in
                tv_season.televisionseasonreview_set.all()]

    @property
    def get_seasons_w_episode_reviews(self):
        return set([tv_season for tv_season in
                    self.televisionseason_set.all() for tv_episode in
                    tv_season.televisionepisode_set.all()
                    if tv_episode.televisionepisodereview_set.all().exists()])

    @property
    def get_year_range(self):
        start_year = ''
        end_year = ''
        if self.televisionseason_set.all().exists():
            start_year = self.televisionseason_set.all().aggregate(
                Min('year_of_release'))['year_of_release__min']
            latest_season = self.televisionseason_set.get(
                season_number=self.televisionseason_set.all().aggregate(
                    Max('season_number'))['season_number__max'])
            end_year = latest_season.season_end_year if \
                latest_season.season_end_year else \
                latest_season.year_of_release

        if not start_year and not end_year:
            return 0, 0
        elif self.is_still_running:
            end_year = ''
        elif start_year == end_year:
            end_year = ''

        return start_year, end_year

    class Meta:
        ordering = ['title_for_sorting']

    def get_absolute_url(self):
        return reverse('tv-series-detail', args=[
            str(self.id), str(self.human_readable_url)])

    def __str__(self):
        return '{main_title}'.format(
            main_title=self.main_title,
            series_type=self.tv_series_type)

    def get_meta_string(self):
        title = 'Title:{title}|'.format(title=str(self.main_title.title))
        tv_series_type = 'TV Series Type:{series_type}|'.format(
            series_type=str(self.tv_series_type))
        if self.is_still_running:
            is_still_running = 'Still Running:Yes|'
        else:
            is_still_running = 'Still Running:No|'
        start_year, end_year = self.get_year_range
        start_year_str = ''
        if start_year:
            start_year_str = 'Start Year:{start_year}|'.format(
                start_year=str(start_year))
        end_year_str = ''
        if end_year:
            end_year_str = 'End Year:{end_year}|'.format(
                end_year=str(end_year))
        return f'{title}{tv_series_type}{is_still_running}{start_year_str}' \
            f'{end_year_str}'


class TelevisionSeason(models.Model):
    tv_series = models.ForeignKey(TelevisionSeries, on_delete=models.SET_NULL,
                                  null=True, help_text='Enter the TV series')
    season_title = models.CharField(
        max_length=50, default='Season', help_text='Enter the title of the '
                                                   'television season')
    season_number = models.IntegerField(
        default=1, help_text='Enter the TV season\'s chronological position '
                             'in the TV series'
                             'as an integer, e.g. "1" for the '
                             'first '
                             'season in the TV series, "2" for the second '
                             'one, etc.')
    year_of_release = models.IntegerField(
        choices=create_release_year_range(),
        help_text='Choose the TV season\'s release year')
    season_end_year = models.IntegerField(choices=create_release_year_range(
    ), blank=True, null=True, help_text='Choose the year when the TV season '
                                        'stopped being aired')
    country_of_origin = models.ManyToManyField(
        Country, help_text='Enter the country of origin')
    poster = models.ImageField(
        upload_to='tv_series_posters/', null=True, blank=True,
        help_text='Upload a poster for the TV season if applicable')
    poster_thumbnail = models.ImageField(
        upload_to='tv_series_posters/thumbnails/', null=True, blank=True,
        help_text='Upload a poster thumbnail for the TV season if applicable')
    duration = models.IntegerField(
        null=True, blank=True, help_text='Enter the duration of the TV '
                                         'Mini-Series in minutes [OPTIONAL]')
    genre = models.ManyToManyField(
        Genre, blank=True, help_text='Enter the TV season\'s genre(s) ['
                                     'OPTIONAL]')
    subgenre = models.ManyToManyField(
        Subgenre, blank=True, help_text='Enter the TV season\'s '
                                        'subgenre [OPTIONAL]')
    microgenre = models.ManyToManyField(
        Microgenre, blank=True, help_text='Enter the TV season\'s '
                                          'microgenre [OPTIONAL]')
    keyword = models.ManyToManyField(
        Keyword, blank=True, help_text='Enter the keyword(s) that best ' \
                                       'describe the TV season [OPTIONAL]')
    movie_participation = models.ManyToManyField(
        MovieParticipation, blank=True,
        help_text='Add the name of the TV season\'s creator, their role and '
                  'the position you want them to appear in the credits')
    description = RichTextField(blank=True, help_text='Provide background '
                                                      'info on this TV season '
                                                      '[OPTIONAL]')
    human_readable_url = models.SlugField(
        help_text="Enter the 'slug',i.e., the human-readable "
                  "URL for the TV serie\'s season", null=True)
    first_created = models.DateField(auto_now_add=True, null=True, blank=True)

    @property
    def nr_of_episode_reviews_for_season(self):
        return len(
            [tv_episode_review for tv_episode in
             self.televisionepisode_set.all() for tv_episode_review
             in tv_episode.televisionepisodereview_set.all()])

    class Meta:
        ordering = ['tv_series', 'season_number']

    def get_absolute_url(self):
        return reverse('tv-season-detail', args=[
            str(self.id), str(self.human_readable_url)])

    def __str__(self):
        return '{tv_series}, Season #{season_num}'.format(
            tv_series=self.tv_series, season_num=self.season_number)

    def get_meta_string(self):
        title = 'Title:{title}|'.format(
            title=str(self.tv_series.main_title.title))
        season_title = 'Season:{season_title}|'.format(
            season_title=str(self.season_title))
        season_number = 'Season Nr.:#{season_nr}|'.format(
            season_nr=str(self.season_number))
        release_year = 'Year:{release_year}|'.format(
            release_year=str(self.year_of_release))
        season_end_year = ''
        if self.season_end_year:
            season_end_year = 'Season End Year:{season_end_year}|'.format(
                season_end_year=str(self.season_end_year))
        country = 'Country:{country}|'.format(country='/'.join(
            [country.name for country in self.country_of_origin.all()]))
        genre = ''
        if self.genre.all():
            genre = 'Genre:{genre}|'.format(genre=','.join(
                [genre.name for genre in self.genre.all()]))
        subgenre = ''
        if self.subgenre.all():
            subgenre = 'Subgenre:{subgenre}|'.format(subgenre=','.join(
                [subgenre.name for subgenre in self.subgenre.all()]))
        microgenre = ''
        if self.microgenre.all():
            microgenre = 'Microgenre:{microgenre}|'.format(
                microgenre=','.join([microgenre.name for microgenre in
                                     self.microgenre.all()]))
        review = ''
        if self.televisionseasonreview_set.all():
            review = 'Our Review:{review}|'.format(
                review=','.join([str(review) for review in
                                 self.televisionseasonreview_set.all()]))

        return f'{title}{season_title}{season_number}{release_year}' \
            f'{season_end_year}{country}{genre}{subgenre}{microgenre}{review}'


class TelevisionEpisode(models.Model):
    tv_season = models.ForeignKey(
        TelevisionSeason, on_delete=models.SET_NULL, null=True,
        help_text='Enter the TV Season this episode belongs to')
    episode_title = models.CharField(
        max_length=50, default='Episode', help_text='Enter the title of the '
                                                    'television episode')
    episode_number = models.IntegerField(
        default=1, help_text='Enter the TV episode\'s chronological position '
                             'in the TV season'
                             'as an integer, e.g. "1" for the '
                             'first '
                             'episode in the TV season, "2" for the second '
                             'one, etc.')
    poster = models.ImageField(
        upload_to='tv_series_posters/', null=True, blank=True,
        help_text='Upload the poster of the movie')
    poster_thumbnail = models.ImageField(
        upload_to='tv_series_posters/thumbnails/', null=True, blank=True,
        help_text='Upload the poster thumbnail')
    duration = models.IntegerField(
        null=True, blank=True, help_text='Enter the duration of the TV '
                                         'episode in minutes [OPTIONAL]')
    genre = models.ManyToManyField(
        Genre, blank=True, help_text='Enter the TV episode\'s genre(s) ['
                                     'OPTIONAL]')
    subgenre = models.ManyToManyField(
        Subgenre, blank=True, help_text='Enter the TV episode\'s '
                                        'subgenre [OPTIONAL]')
    microgenre = models.ManyToManyField(
        Microgenre, blank=True, help_text='Enter the TV episode\'s '
                                          'microgenre [OPTIONAL]')
    keyword = models.ManyToManyField(
        Keyword, blank=True, help_text='Enter the keyword(s) that best ' \
                                       'describe the TV episode ['
                                       'OPTIONAL]')
    movie_participation = models.ManyToManyField(
        MovieParticipation, blank=True,
        help_text='Add the name of the TV episode creator, their role and the '
                  'position you want them to appear in the credits')

    class Meta:
        ordering = ['tv_season', 'episode_number']

    def __str__(self):
        return '{tv_season}, Ep. #{episode_number}'.format(
            tv_season=self.tv_season, episode_number=self.episode_number)


class TelevisionSeasonReview(Review):
    reviewed_tv_season = models.ForeignKey(
        TelevisionSeason, null=True,
        help_text='Enter the TV season that you\'re reviewing')
    mov_review_page_description = models.CharField(
        max_length=155, default='Click on the link to see what we have to '
                                'say about this flick.')
    human_readable_url = models.SlugField(
        null=True, help_text="Enter the 'slug',i.e., the human-readable "
                             "URL for the TV season review")

    @property
    def previous_and_next_season_review(self):
        previous_season_review = None
        next_season_review = None
        current_season_nr = self.reviewed_tv_season.season_number
        highest_season_nr = \
            self.reviewed_tv_season.tv_series.televisionseason_set.all(
            ).aggregate(Max('season_number'))['season_number__max']

        if current_season_nr != 1:
            if self.reviewed_tv_season.tv_series.televisionseason_set.all(
            ).filter(season_number=current_season_nr - 1).exists():
                previous_season_review = self.reviewed_tv_season.tv_series\
                    .televisionseason_set.all().get(
                    season_number=current_season_nr - 1
                ).televisionseasonreview_set.all()

        if current_season_nr != highest_season_nr:
            if self.reviewed_tv_season.tv_series.televisionseason_set.all(
            ).filter(season_number=current_season_nr + 1).exists():
                next_season_review = self.reviewed_tv_season.tv_series.\
                    televisionseason_set.all().get(
                    season_number=current_season_nr + 1). \
                    televisionseasonreview_set.all()

        return previous_season_review, next_season_review

    class Meta:
        ordering = ['reviewed_tv_season']

    def get_absolute_url(self):
        return reverse('tv-season-review',
                       args=[str(self.id), str(self.human_readable_url)])

    def __str__(self):
            return '{tv_season}, by {reviewer}'.format(
                tv_season=self.reviewed_tv_season, reviewer=self.review_author)


class TelevisionEpisodeReview(Review):
    reviewed_tv_episode = models.ForeignKey(
        TelevisionEpisode, null=True,
        help_text='Enter the TV episode that you\'re reviewing')
    mov_review_page_description = models.CharField(
        max_length=155, default='Click on the link to see what we have to '
                                'say about this flick.')
    human_readable_url = models.SlugField(
        null=True, help_text='Enter the "slug",i.e., the human-readable URL '
                             'for the TV episode review')

    @property
    def previous_and_next_episode_review(self):
        previous_episode_review = None
        next_episode_review = None
        current_episode_nr = self.reviewed_tv_episode.episode_number
        highest_episode_nr = \
            self.reviewed_tv_episode.tv_season.televisionepisode_set.all(
                ).aggregate(Max('episode_number'))['episode_number__max']

        if current_episode_nr != 1:
            if self.reviewed_tv_episode.tv_season.televisionepisode_set.all(
                    ).filter(episode_number=current_episode_nr-1).exists():
                previous_episode_review = self.reviewed_tv_episode.tv_season.\
                    televisionepisode_set.all().get(
                        episode_number=current_episode_nr-1
                ).televisionepisodereview_set.all()

        if current_episode_nr != highest_episode_nr:
            if self.reviewed_tv_episode.tv_season.televisionepisode_set.all(
            ).filter(episode_number=current_episode_nr+1).exists():
                next_episode_review = self.reviewed_tv_episode.tv_season.\
                    televisionepisode_set.all().get(
                    episode_number=current_episode_nr+1).\
                    televisionepisodereview_set.all()

        return previous_episode_review, next_episode_review

    class Meta:
        ordering = ['reviewed_tv_episode']

    def get_absolute_url(self):
        return reverse('tv-episode-review',
                       args=[str(self.id), str(self.human_readable_url)])

    def __str__(self):
            return '{tv_episode}, by {reviewer}'.format(
                tv_episode=self.reviewed_tv_episode,
                reviewer=self.review_author)


class PickedReview(models.Model):
    picked_review = models.OneToOneField(MovieReview)
    date_added = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return 'review: {picked_review} picked on: {date}'.format(
            picked_review=self.picked_review, date=self.date_added)


def get_random_review(latest_review, featured_review):
    if featured_review is not None:
        qs = MovieReview.objects.all().exclude(pk__in=[latest_review.pk,
                                                       featured_review.pk])
    else:
        qs = MovieReview.objects.all().exclude(pk=latest_review.pk)

    if not qs:
        return None
    max_pk = qs.aggregate(models.Max('pk'))['pk__max']
    min_pk = qs.aggregate(models.Min('pk'))['pk__min']
    counter = min_pk

    while counter <= max_pk:
        random_pk = random.randint(min_pk, max_pk)
        try:
            return qs.get(pk=random_pk)
        except qs.model.DoesNotExist:
            pass
        counter += 1
    # default return
    return qs.get(pk=min_pk)
