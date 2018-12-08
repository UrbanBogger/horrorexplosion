from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    name = 'reviews'

    def ready(self):
        from mov_similarity_calculator import calculate_movie_similarity
        calculate_movie_similarity.find_and_save_similar_movies()
        from mov_similarity_calculator import similar_mov_updater
        similar_mov_updater.start()
