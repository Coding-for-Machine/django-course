# project/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from courses.api import api_course
from lessons.problems_api import problems_api
from lessons.api import router  # Routerni import qilish
from users.api import user_router
# ✅ `urls.py` fayliga API'ni qo‘shish
from solution.api import solution_url_api

from .api import api

api.add_router("/", api_course)
api.add_router('lessons/', router)
api.add_router('lessons1/', problems_api)
api.add_router('result/', solution_url_api)
api.add_router("/user/", user_router)



urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),  # Kurs API
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
