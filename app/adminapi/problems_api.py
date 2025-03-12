from ninja import Router
from ninja.errors import HttpError
from pydantic import BaseModel
from typing import List
from datetime import datetime
from .auth_permission import IsStaff, IsSuperuser
from lessons.models import Problem, Language

problems_router_api = Router()

# ---------------- problem schemas -----------------
class ProblemList(BaseModel):
    id: int
    lesson: int
    languages: List[int]  # languages ni List[int] qilib o'zgartirdik
    title: str
    slug: str
    description: str
    difficulty: str
    user: int
    created_at: datetime
    updated_at: datetime

class ProblemCreate(BaseModel):
    lesson: int
    languages: List[int]  # languages ni List[int] qilib o'zgartirdik
    title: str
    description: str
    difficulty: str
    user: int

# ---------------- problem crud --------------------

# problem get
@problems_router_api.get("/", response=List[ProblemList], auth=[IsSuperuser(), IsStaff()])
def problems_get_api(request):
    problems = Problem.objects.all()
    return [
        {
            "id": problem.id,
            "lesson": problem.lesson.id,
            "languages": [lang.id for lang in problem.languages.all()],  # languages ni ro'yxat shaklida qaytarish
            "title": problem.title,
            "slug": problem.slug,
            "description": problem.description,
            "difficulty": problem.difficulty,
            "user": problem.user.id,
            "created_at": problem.created_at,
            "updated_at": problem.updated_at,
        }
        for problem in problems
    ]

# problem get slug
@problems_router_api.get("/{slug}", response=ProblemList, auth=[IsSuperuser(), IsStaff()])
def problems_get_slug_api(request, slug: str):
    try:
        problem = Problem.objects.get(slug=slug)
        return {
            "id": problem.id,
            "lesson": problem.lesson.id,
            "languages": [lang.id for lang in problem.languages.all()],  # languages ni ro'yxat shaklida qaytarish
            "title": problem.title,
            "slug": problem.slug,
            "description": problem.description,
            "difficulty": problem.difficulty,
            "user": problem.user.id,
            "created_at": problem.created_at,
            "updated_at": problem.updated_at,
        }
    except Problem.DoesNotExist:
        raise HttpError(404, "Problem topilmadi!")
    except Exception as e:
        raise HttpError(500, f"Xato yuz berdi: {str(e)}")

# created
@problems_router_api.post("/create/", response=ProblemList, auth=[IsSuperuser(), IsStaff()])
def problems_created(request, data: ProblemCreate):
    try:
        # Problem obyektini yaratish
        problem = Problem.objects.create(
            lesson_id=data.lesson,
            title=data.title,
            description=data.description,
            difficulty=data.difficulty,
            user_id=data.user,
        )
        # languages ni qo'shish
        for lang_id in data.languages:
            language = Language.objects.get(id=lang_id)
            problem.languages.add(language)
        return {
            "id": problem.id,
            "lesson": problem.lesson.id,
            "languages": [lang.id for lang in problem.languages.all()],
            "title": problem.title,
            "slug": problem.slug,
            "description": problem.description,
            "difficulty": problem.difficulty,
            "user": problem.user.id,
            "created_at": problem.created_at,
            "updated_at": problem.updated_at,
        }
    except Exception as e:
        raise HttpError(400, f"Problem yaratishda xato: {str(e)}")

# problem update
@problems_router_api.put("/update/{slug}", response=ProblemList, auth=[IsSuperuser(), IsStaff()])
def problems_update(request, slug: str, data: ProblemCreate):
    try:
        problem = Problem.objects.get(slug=slug)
        # Oddiy maydonlarni yangilash
        problem.lesson_id = data.lesson
        problem.title = data.title
        problem.description = data.description
        problem.difficulty = data.difficulty
        problem.user_id = data.user
        problem.save()
        # languages ni yangilash
        problem.languages.clear()
        for lang_id in data.languages:
            language = Language.objects.get(id=lang_id)
            problem.languages.add(language)
        return {
            "id": problem.id,
            "lesson": problem.lesson.id,
            "languages": [lang.id for lang in problem.languages.all()],
            "title": problem.title,
            "slug": problem.slug,
            "description": problem.description,
            "difficulty": problem.difficulty,
            "user": problem.user.id,
            "created_at": problem.created_at,
            "updated_at": problem.updated_at,
        }
    except Problem.DoesNotExist:
        raise HttpError(404, "Problem topilmadi!")
    except Exception as e:
        raise HttpError(400, f"Problemni yangilashda xato: {str(e)}")

# problem delete
@problems_router_api.delete("/delete/{slug}",  auth=[IsSuperuser(), IsStaff()])
def problems_delete(request, slug: str):
    try:
        problem = Problem.objects.get(slug=slug)
        problem.delete()
        return {"success": True, "message": "Problem muvaffaqiyatli o'chirildi"}
    except Problem.DoesNotExist:
        raise HttpError(404, "Problem topilmadi!")
    except Exception as e:
        raise HttpError(400, f"Problemni o'chirishda xato: {str(e)}")