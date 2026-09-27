#!/bin/sh

# Останавливать выполнение при возникновении ошибок
set -e

# Применение миграций базы данных
python manage.py migrate

# Сбор статических файлов для Nginx
python manage.py collectstatic --no-input

# Запуск WSGI-сервера Gunicorn
gunicorn myproject.wsgi:application --bind 0.0.0.0:8000 --workers 3 