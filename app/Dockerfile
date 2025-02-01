# Python image'dan foydalanamiz
FROM python:3.11-slim

# Ishchi katalogni belgilash
WORKDIR /app

# Talablar faylini konteynerga nusxalash
COPY requirements.txt /app/

# Talablarni o'rnatish
RUN pip install --no-cache-dir -r requirements.txt

# Django loyihasining manbasini konteynerga nusxalash
COPY . /app/

# Entrypoint skriptini nusxalash va unga ruxsat berish
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Skriptni bajarish
ENTRYPOINT ["/entrypoint.sh"]

# Portni ochish
EXPOSE 8000

# Django serverini ishga tushurish (default)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
