release: python3 manage.py migrate
web: gunicorn horrorexplosion.wsgi --log-file -

release: python3 manage.py find_similar_movies
web: gunicorn horrorexplosion.wsgi --log-file -
