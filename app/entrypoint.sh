#!/bin/bash

if [ "$DJANGO_ENV" = "production" ]; then
    echo "Ishlab chiqarish muhitiga o'tilmoqda..."
    # Agar ishlab chiqarish bo'lsa, collectstatic ishlatilsin
    python manage.py collectstatic --noinput
else
    echo "Ishlab chiqish muhitida..."
fi

echo "Migratsiyalarni bajarish..."
python manage.py migrate

echo "Superuser yaratish tekshirilmoqda..."
python manage.py createsuperuser --noinput || echo "Superuser allaqachon mavjud"

# Keshni tozalash
echo "Keshni tozalash..."
python manage.py clear_cache
echo "Gunicorn serverini ishga tushurish..."
exec gunicorn app.wsgi:application --bind 0.0.0.0:8000 

