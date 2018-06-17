from django.test import TestCase
from django.db.models import Max, Min
from reviews.models import Genre, Subgenre, Keyword, WebsiteMetadescriptor,\
    Reviewer, MovieCreator, CreativeRole, Title, Movie, MovieReview, \
    Country, MovieParticipation, create_release_year_range, \
    sort_titles_with_stop_word, Grade, get_random_review
import datetime
import random

class MovieMetadescriptorsCommonCodeTest(TestCase):
    model_id = 2
    field_label = ''

    @classmethod
    def setUpTestData(cls):
        # create a few sample MovieMEtadescriptors objects
        Genre.objects.create(name='Horror')
        Genre.objects.create(name='Thriller')
        Genre.objects.create(name='Comedy')

    @staticmethod
    def get_object_by_id(object_id):
        return Genre.objects.get(id=object_id)

    def get_obj_by_id_experimental(self, metadescriptor_class, object_id):
        return metadescriptor_class.objects.get(id=object_id)

    def test_name_label(self):
        self.movie_metadescriptor = self.get_obj_by_id_experimental(
            Genre, self.model_id)
        self.field_label = self.movie_metadescriptor\
            ._meta.get_field('name').verbose_name
        self.assertEquals(self.field_label, 'name')

    def test_description_label(self):
        self.movie_metadescriptor = self.get_object_by_id(self.model_id)
        self.field_label = self.movie_metadescriptor._meta.get_field(
            'description').verbose_name
        self.assertEquals(self.field_label, 'description')

    def test_description_field_length(self):
        expected_description_field_length = 1000
        self.movie_metadescriptor = self.get_object_by_id(self.model_id)
        description_field_length = self.movie_metadescriptor._meta.get_field(
            'description').max_length
        self.assertEquals(expected_description_field_length,
                          description_field_length)

    def test_default_name_field_length(self):
        expected_name_field_length = 50
        self.movie_metadescriptor = self.get_object_by_id(self.model_id)
        description_field_length = self.movie_metadescriptor._meta.get_field(
            'name').max_length
        self.assertEquals(expected_name_field_length,
                          description_field_length)

    def test_description_is_optional(self):
        is_optional = True
        self.movie_metadescriptor = self.get_object_by_id(self.model_id)
        description_field_declared_blank = self.movie_metadescriptor\
            ._meta.get_field('description').blank
        self.assertEquals(is_optional, description_field_declared_blank)

    def test_description_empty_string_by_default(self):
        empty_string = ''
        self.movie_metadescriptor = self.get_object_by_id(self.model_id)
        description_field_default_value = self.movie_metadescriptor\
            ._meta.get_field('description').default
        self.assertEquals(empty_string, description_field_default_value)

    def test_movie_metadescriptors_ordered_in_ascending_order(self):
        ordered_genres = ['Comedy', 'Horror', 'Thriller']
        all_genre_objects = Genre.objects.all()
        all_genres = [all_genre_objects[index].name for index, genre in
                           enumerate(all_genre_objects)]
        self.assertEquals(ordered_genres, all_genres)

    def test_name_field_describes_the_model(self):
        expected_model_description = 'Thriller'
        self.movie_metadescriptor = self.get_object_by_id(self.model_id)
        model_description = self.movie_metadescriptor.__str__()
        self.assertEquals(expected_model_description, model_description)

    # include the Genre test as an inner class because of database
    # consistency concerns
    class GenreModelTest(TestCase):
        def test_name_field_help_txt_correct(self):
            expected_help_txt = 'Enter the name of the genre'
            genre = self.get_object_by_id(1)
            name_field_help_txt = genre._meta.get_field('name').help_text
            self.assertEquals(expected_help_txt, name_field_help_txt)


class SubgenreModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Subgenre.objects.create(name='Monster Movie')

    @staticmethod
    def get_subgenre_by_id(subgenre_id):
        return Subgenre.objects.get(id=subgenre_id)

    def test_name_field_help_txt_correct(self):
        expected_help_text = 'Enter the name of the subgenre'
        subgenre = self.get_subgenre_by_id(1)
        name_field_help_txt = subgenre._meta.get_field('name').help_text
        self.assertEquals(expected_help_text, name_field_help_txt)


class KeywordModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Keyword.objects.create(name='zombies')

    @staticmethod
    def get_keyword_by_id(keyword_id):
        return Keyword.objects.get(id=keyword_id)

    def test_name_field_length(self):
        expected_name_field_length = 100
        keyword = self.get_keyword_by_id(1)
        name_field_length = keyword._meta.get_field('name').max_length
        self.assertEquals(expected_name_field_length, name_field_length)

    def test_name_field_help_txt(self):
        expected_help_text = 'Enter the keyword (or a keyword phrase)'
        keyword = self.get_keyword_by_id(1)
        help_text = keyword._meta.get_field('name').help_text
        self.assertEquals(expected_help_text, help_text)


class WebsiteMetadescriptorsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        WebsiteMetadescriptor.objects.create(
            website_name='The Horror Explosion',
            contact_info='horror_explosion@someemail.com',
            mission_statement='Our mission statement')

    @staticmethod
    def get_website_metadescriptor_by_id(website_metadescriptor_id):
        return WebsiteMetadescriptor.objects.get(id=website_metadescriptor_id)

    def test_website_name_and_contact_info_field_length(self):
        expected_field_length = 50
        website_metadescriptor = self.get_website_metadescriptor_by_id(1)
        website_name_field_length = website_metadescriptor._meta.get_field(
            'website_name').max_length
        contact_info_field_length = website_metadescriptor._meta.get_field(
            'contact_info').max_length
        self.assertEquals(expected_field_length, website_name_field_length)
        self.assertEquals(expected_field_length, contact_info_field_length)

    def test_mission_statement_field_length(self):
        expected_field_length = 1000
        website_metadescriptor = self.get_website_metadescriptor_by_id(1)
        mission_statement_field_length = \
            website_metadescriptor._meta.get_field(
                'mission_statement').max_length
        self.assertEquals(expected_field_length,
                          mission_statement_field_length)

    def test_mission_statement_field_is_optional(self):
        website_metadescriptor = self.get_website_metadescriptor_by_id(1)
        field_is_optional = website_metadescriptor._meta.get_field(
            'mission_statement').blank
        self.assertTrue(field_is_optional)

    def test_contact_info_field_help_msg(self):
        expected_help_txt = 'Enter a contact email'
        website_metadescriptor = self.get_website_metadescriptor_by_id(1)
        help_txt = website_metadescriptor._meta.get_field(
            'contact_info').help_text
        self.assertEquals(expected_help_txt, help_txt)

    def test_self_description_txt(self):
        expected_self_description_txt = \
            'Website name: {website_name}\nContact Info: {' \
            'contact_info}\nMission Statement: {mission_statement}\n'.format(
                website_name='The Horror Explosion',
                contact_info='horror_explosion@someemail.com',
                mission_statement='Our mission statement')
        website_metadescriptor = self.get_website_metadescriptor_by_id(1)
        description_txt = website_metadescriptor.__str__()
        self.assertEquals(expected_self_description_txt, description_txt)


class PersonModelCommonCodeTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Reviewer.objects.create(first_name='M', last_name='S')
        MovieCreator.objects.create(first_name='George', middle_name='A.',
                                    last_name='Romero')
        MovieCreator.objects.create(first_name='John', last_name='Carpenter')
        MovieCreator.objects.create(first_name='Jennifer',
                                    middle_name='Jason', last_name='Leigh')

    @staticmethod
    def get_person_object_by_id(person_class, person_id):
        return person_class.objects.get(id=person_id)

    def test_reviewer_model__self_description(self):
        expected_description = 'MS'
        reviewer_object = self.get_person_object_by_id(Reviewer, 1)
        description = reviewer_object.__str__()
        self.assertEquals(expected_description, description)

    def test_middle_name_optional(self):
        reviewer_object = self.get_person_object_by_id(Reviewer, 1)
        is_optional = reviewer_object._meta.get_field('middle_name').blank
        self.assertTrue(is_optional)

    def test_biography_optional(self):
        reviewer_object = self.get_person_object_by_id(Reviewer, 1)
        is_optional = reviewer_object._meta.get_field('biography').blank
        self.assertTrue(is_optional)

    def test_name_fields_length(self):
        expected_field_length = 50
        reviewer_object = self.get_person_object_by_id(Reviewer, 1)
        first_name_field_length = reviewer_object._meta.get_field(
            'first_name').max_length
        middle_name_field_length = reviewer_object._meta.get_field(
            'middle_name').max_length
        last_name_field_length = reviewer_object._meta.get_field(
            'last_name').max_length
        self.assertEquals(expected_field_length, first_name_field_length)
        self.assertEquals(expected_field_length, middle_name_field_length)
        self.assertEquals(expected_field_length, last_name_field_length)

    def test_biography_field_length(self):
        expected_field_length = 1000
        reviewer_object = self.get_person_object_by_id(Reviewer, 1)
        biography_field_length =reviewer_object._meta.get_field(
            'biography').max_length
        self.assertEquals(expected_field_length, biography_field_length)

    def test_movie_creator_name_rendered_correctly(self):
        george_romero = self.get_person_object_by_id(MovieCreator, 1)
        john_carpenter = self.get_person_object_by_id(MovieCreator, 2)
        jennifer_jason_leigh = self.get_person_object_by_id(MovieCreator, 3)
        self.assertEquals('George A. Romero', george_romero.__str__())
        self.assertEquals('John Carpenter', john_carpenter.__str__())
        self.assertEquals('Jennifer Jason Leigh',
                          jennifer_jason_leigh.__str__())

    def test_people_sorted_by_surname(self):
        expected_order = [
            'John Carpenter', 'Jennifer Jason Leigh', 'George A. Romero']
        all_movie_creator_objects = MovieCreator.objects.all()
        ordered_movie_creators = [movie_creator.__str__() for
                                  movie_creator in all_movie_creator_objects]
        self.assertEquals(expected_order, ordered_movie_creators)


class CreativeRoleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CreativeRole.objects.create(role_name='Director')
        CreativeRole.objects.create(role_name='Actor')
        CreativeRole.objects.create(role_name='Writer')

    @staticmethod
    def get_role_object_by_id(role_id):
        return CreativeRole.objects.get(id=role_id)

    def test_role_name_field_length(self):
        expected_length = 50
        role = self.get_role_object_by_id(1)
        role_name_field_length = role._meta.get_field('role_name').max_length
        self.assertEquals(expected_length, role_name_field_length)

    def test_role_name_field_help_text(self):
        expected_help_text = 'Enter the creative role that a person might ' \
                             'have, e.g. Director, Editor, Writer, etc.'
        role = self.get_role_object_by_id(1)
        role_name_field_help_txt = role._meta.get_field('role_name').help_text
        self.assertEquals(expected_help_text, role_name_field_help_txt)

    def test_role_name_displayed_properly(self):
        expected_display = 'Director'
        role = self.get_role_object_by_id(1)
        self.assertEquals(expected_display, role.__str__())

    def test_roles_ordered_correctly(self):
        expected_order = ['Actor', 'Director', 'Writer']
        all_role_objects = CreativeRole.objects.all()
        ordered_role_objects = [role.__str__() for role in all_role_objects]
        self.assertEquals(expected_order, ordered_role_objects)


class MovieTitleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Title.objects.create(title='Hostel')

    @staticmethod
    def get_title_object_by_id(title_id):
        return Title.objects.get(id=title_id)

    def test_title_field_length(self):
        expected_length = 100
        movie_title = self.get_title_object_by_id(1)
        title_field_length = movie_title._meta.get_field('title').max_length
        self.assertEquals(expected_length, title_field_length)

    def test_title_displayed_correctly(self):
        expected_title_display = 'Hostel'
        movie_title = self.get_title_object_by_id(1)
        self.assertEquals(expected_title_display, movie_title.__str__())


class MovieTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        hostel = Title.objects.create(title='Hostel')
        hostel_2 = Title.objects.create(title='Hostel: Part II')
        amytiville_horror = Title.objects.create(title='The Amytiville Horror')
        cabin_fever = Title.objects.create(title='Cabin Fever')
        christmas_horror_story = Title.objects.create(
            title='A Christmas Horror Story')
        quiet_place = Title.objects.create(title='A Quiet Place')
        conjuring = Title.objects.create(title='The Conjuring')
        days_later = Title.objects.create(title='28 Days Later')
        one_four_zero_eight = Title.objects.create(title='1408')
        year_of_release = 2005
        duration = 94

        Movie.objects.create(
            main_title=hostel, year_of_release=year_of_release,
            duration=duration)
        Movie.objects.create(
            main_title=hostel_2, year_of_release=year_of_release,
            duration=duration)
        Movie.objects.create(
            main_title=amytiville_horror, year_of_release=year_of_release,
            duration=duration)
        Movie.objects.create(
            main_title=cabin_fever, year_of_release=year_of_release,
            duration=duration)
        Movie.objects.create(
            main_title=christmas_horror_story, year_of_release=year_of_release,
            duration=duration)
        Movie.objects.create(
            main_title=quiet_place, year_of_release=year_of_release,
            duration=duration)
        Movie.objects.create(
            main_title=conjuring, year_of_release=year_of_release,
            duration=duration)
        Movie.objects.create(
            main_title=days_later, year_of_release=year_of_release,
            duration=duration)
        Movie.objects.create(
            main_title=one_four_zero_eight, year_of_release=year_of_release,
            duration=duration)

    def test_release_year_boundary_values(self):
        movie = Movie()
        release_year_list = create_release_year_range()
        release_start_year = 1895
        now = datetime.datetime.now()
        current_year = now.year
        self.assertEquals(release_start_year, release_year_list[0][0])
        self.assertEquals(current_year, release_year_list[
            len(release_year_list) - 1][0])

    def test_movie_ordering(self):
        movies = Movie.objects.all()
        print('Unsorted movies: ' + str(movies))
        sorted_movies = sort_titles_with_stop_word(movies)
        print('Sorted movies: ' + str(sorted_movies))

    def test_only_reviewed_movies_retrieved(self):
        all_movies = Movie.objects.all()
        test_review01 = MovieReview.objects.create(
            reviewed_movie=all_movies[0], review_text='Horror movie review',
            grade='2.5', date_created=datetime.datetime.now())
        test_review02 = MovieReview.objects.create(
            reviewed_movie=all_movies[len(all_movies) -1],
            review_text='Another Horror movie review',
            grade='3.5', date_created=datetime.datetime.now())
        test_author = Reviewer.objects.create(first_name='M.', last_name='S.')
        test_review01.review_author.add(test_author)
        test_review02.review_author.add(test_author)
        reviewed_movies = [movie for movie in
                           Movie.objects.filter(moviereview__isnull=False)]
        self.assertEquals(2, len(reviewed_movies))

    def test_multiple_reviews_per_movie_correctly_displayed(self):
        all_movies = Movie.objects.all()
        test_review01 = MovieReview.objects.create(
            reviewed_movie=all_movies[0], review_text='Horror movie review',
            grade='2.5', date_created=datetime.datetime.now())
        test_review02 = MovieReview.objects.create(
            reviewed_movie=all_movies[0],
            review_text='Another Horror movie review',
            grade='3.5', date_created=datetime.datetime.now())
        test_author01 = Reviewer.objects.create(
            first_name='M.', last_name='S.')
        test_author02 = Reviewer.objects.create(
            first_name='D.', last_name='D.')
        test_review01.review_author.add(test_author01)
        test_review02.review_author.add(test_author02)

        test_movie = Movie.objects.get(id=1)
        movie_reviews = test_movie.moviereview_set.all()
        for review in movie_reviews:
            self.assertRegexpMatches(
                review.review_text + ' graded with '
                + review.grade + ' stars', r'\w+\s(\d\.\d){1}\s\w+')


class ReviewerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_reviewer = Reviewer.objects.create(
            first_name='M.', last_name='S.')

    def test_string_representation_of_reviewer_correct(self):
        reviewer = Reviewer.objects.get(pk=1)
        self.assertEquals('M.S.', reviewer.__str__())


class MovieReviewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        year_of_release = 2005
        duration = 94
        hostel = Title.objects.create(title='Hostel')
        hostel_2 = Title.objects.create(title='Hostel: Part II')
        amytiville_horror = Title.objects.create(title='The Amytiville Horror')
        cabin_fever = Title.objects.create(title='Cabin Fever')
        test_author = Reviewer.objects.create(first_name='D.', last_name='D.')
        grade = Grade.objects.create(grade_numerical=2.5)
        test_movie = Movie.objects.create(
            main_title=Title.objects.create(title='Hostel'),
            year_of_release=2005, duration=94)
        test_movie02 = Movie.objects.create(
            main_title=hostel, year_of_release=year_of_release,
            duration=duration)
        test_movie03 = Movie.objects.create(
            main_title=hostel_2, year_of_release=year_of_release,
            duration=duration)
        test_movie04 = Movie.objects.create(
            main_title=amytiville_horror, year_of_release=year_of_release,
            duration=duration)
        test_movie05 = Movie.objects.create(
            main_title=cabin_fever, year_of_release=year_of_release,
            duration=duration)
        test_review = MovieReview.objects.create(
            reviewed_movie=test_movie, review_text='Some review txt',
            date_created=datetime.datetime(2018, 6, 14))
        test_review_02 = MovieReview.objects.create(
            reviewed_movie=test_movie02, review_text='Review 2',
            date_created=datetime.datetime(2018, 6, 15))
        test_review_03 = MovieReview.objects.create(
            reviewed_movie=test_movie03, review_text='Review 3',
            date_created=datetime.datetime(2018, 6, 16))
        test_review_04 = MovieReview.objects.create(
            reviewed_movie=test_movie04, review_text='Review 3',
            date_created=datetime.datetime(2018, 6, 17))
        #test_review.review_author.add(test_author)

    def test_string_representation_of_review_correct(self):
        review_object = MovieReview.objects.get(pk=1)
        self.assertEquals('Hostel (2005) by D.D.', review_object.__str__())

