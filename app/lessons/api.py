from ninja import Router
from django.shortcuts import get_object_or_404
from .models import Lesson, Problem, TestCase
from .schemas import LessonSchema  # LessonSchema Pydantic modelini import qilamiz
from django.http import JsonResponse

from users.api_auth import api_auth_user_required
router = Router()

@router.get("/{slug}", response=LessonSchema, auth=api_auth_user_required)
def get_lesson_by_slug(request, slug: str):
    # Slug orqali Lesson obyektini olish
    lesson = get_object_or_404(Lesson, slug=slug)
    # Lessonga tegishli muammolarni olish
    problems = Problem.objects.filter(lesson=lesson)
    
    # Lesson ma'lumotlarini yaratish
    lesson_data ={"lesson": [{
        "id": lesson.id,
        "title": lesson.title,
        "slug": lesson.slug,
        "lesson_type": lesson.lesson_type,
        "locked": lesson.locked,
        "preview": lesson.preview,
        "created_at": lesson.created_at,
        "updated_at": lesson.updated_at,
        "problems": [
            {
                "id": problem.id,
                "title": problem.title,
                "description": problem.description,
                "difficulty": problem.difficulty,
                "created_at": problem.created_at,
                "updated_at": problem.updated_at,
            }
            for problem in problems
        ]
    }]}

    return JsonResponse(lesson_data)
