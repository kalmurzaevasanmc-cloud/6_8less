echo "🔄 Применяем миграции..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "🧹 Собираем статику..."
python manage.py collectstatic --noinput

echo "🚀 Запускаем сервер..." 
exec python manage.py runserver 0.0.0.0:8000 