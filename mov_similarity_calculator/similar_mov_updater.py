from datetime import datetime
import os

from apscheduler.schedulers.background import BackgroundScheduler
from mov_similarity_calculator.calculate_movie_similarity import \
    find_and_save_similar_movies


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=find_and_save_similar_movies, trigger='interval',
                      hours=22)
    scheduler.start()
