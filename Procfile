release: python manage.py makemigrations; python manage.py migrate
web: gunicorn recipesite.wsgi --log-file -
