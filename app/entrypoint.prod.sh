#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

echo "INSERT INTO django_migrations (app, name, applied) VALUES ('users', '0001_initial', CURRENT_TIMESTAMP);" | python manage.py dbshell
echo "UPDATE django_content_type SET app_label = 'users' WHERE app_label = 'auth' and model = 'user';" | python manage.py dbshell
python manage.py migrate
python manage.py collectstatic --no-input --clear

exec "$@"