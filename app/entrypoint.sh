#!/bin/bash

# Muhitni tekshirish (staging yoki production)
if [ "$DJANGO_ENV" = "production" ]; then
    echo "Ishlab chiqarish muhitiga o'tilmoqda..."
    # Agar ishlab chiqarish bo'lsa, collectstatic ishlatilsin
    python manage.py collectstatic --noinput
else
    echo "Ishlab chiqish muhitida..."
fi

# Migratsiyalarni bajarish
echo "Migratsiyalarni bajarish..."
python manage.py migrate

# Superuser yaratish (agar mavjud bo'lmasa)
echo "Superuser yaratish tekshirilmoqda..."
python manage.py createsuperuser --noinput || echo "Superuser allaqachon mavjud"

# Keshni tozalash
echo "Keshni tozalash..."
python manage.py clear_cache

# Log faylini yaratish va yangilash
LOG_FILE="/app/logs/django.log"
echo "Django serveri boshlanishi..." > $LOG_FILE
echo "Migratsiyalarni bajarish..." >> $LOG_FILE
python manage.py migrate >> $LOG_FILE 2>&1
echo "Superuser yaratish..." >> $LOG_FILE
python manage.py createsuperuser --noinput >> $LOG_FILE 2>&1 || echo "Superuser allaqachon mavjud" >> $LOG_FILE
echo "Keshni tozalash..." >> $LOG_FILE
python manage.py clear_cache >> $LOG_FILE 2>&1

# Gunicorn serverini ishga tushurish (production uchun)
if [ "$DJANGO_ENV" = "production" ]; then
    echo "Gunicorn serverini ishga tushurish..."
    exec gunicorn myproject.wsgi:application --bind 0.0.0.0:8000 >> $LOG_FILE 2>&1
else
    # Django serverini ishga tushurish (staging uchun)
    echo "Django serveri ishga tushurilmoqda..."
    exec "$@" >> $LOG_FILE 2>&1
fi
