from ninja import Router, QueryEx
from ninja.errors import HttpError
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .auth_permission import IsStaff, IsSuperuser
from savollar.models import Quiz
from courses.models import MyModules

# -------------- schema quiz ------------
class QuizSchemaList(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    modules: List[int]  # modules ni List[int] qilib o'zgartirdik
    time_limit: int
    user: int  # user ni int qilib o'zgartirdik
    created_at: datetime
    updated_at: datetime

class QuizSchemaCreate(BaseModel):
    title: str
    slug: str
    description: str
    modules: List[int]  # modules ni List[int] qilib o'zgartirdik
    time_limit: int
    user: int  # user ni int qilib o'zgartirdik

class QuizSchemaUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    modules: Optional[List[int]] = None  # modules ni List[int] qilib o'zgartirdik
    time_limit: Optional[int] = None
    user: Optional[int] = None  # user ni int qilib o'zgartirdik

# -------------- crud quiz --------------

quize_router = Router()

# Get all quizzes
@quize_router.get("/", response=List[QuizSchemaList], auth=[IsSuperuser(), IsStaff()])
def quize_get(request):
    quizzes = Quiz.objects.all()
    return [
        {
            "id": quiz.id,
            "title": quiz.title,
            "slug": quiz.slug,
            "description": quiz.description,
            "modules": [module.id for module in quiz.modules.all()],  # modules ni ro'yxat shaklida qaytarish
            "time_limit": quiz.time_limit,
            "user": quiz.user.id,  # user ni int qilib qaytarish
            "created_at": quiz.created_at,
            "updated_at": quiz.updated_at,
        }
        for quiz in quizzes
    ]

# Create a new quiz
@quize_router.post("create/", response=QuizSchemaList, auth=[IsSuperuser(), IsStaff()])
def quize_create(request, payload: QuizSchemaCreate):
    try:
        # Quiz obyektini yaratish
        quiz = Quiz.objects.create(
            title=payload.title,
            slug=payload.slug,
            description=payload.description,
            time_limit=payload.time_limit,
            user_id=payload.user,  # user_id orqali bog'lash
        )
        # modules ni qo'shish
        for module_id in payload.modules:
            module = MyModules.objects.get(id=module_id)
            quiz.modules.add(module)
        return {
            "id": quiz.id,
            "title": quiz.title,
            "slug": quiz.slug,
            "description": quiz.description,
            "modules": [module.id for module in quiz.modules.all()],
            "time_limit": quiz.time_limit,
            "user": quiz.user.id,
            "created_at": quiz.created_at,
            "updated_at": quiz.updated_at,
        }
    except Exception as e:
        raise HttpError(400, f"Quiz yaratishda xato: {str(e)}")

# Update a quiz
@quize_router.put("update/{quiz_id}", response=QuizSchemaList, auth=[IsSuperuser(), IsStaff()])
def quize_update(request, quiz_id: int, payload: QuizSchemaUpdate):
    try:
        quiz = Quiz.objects.filter(id=quiz_id).first()
        if not quiz:
            raise HttpError(404, "Quiz not found")
        
        # Oddiy maydonlarni yangilash
        if payload.title:
            quiz.title = payload.title
        if payload.slug:
            quiz.slug = payload.slug
        if payload.description:
            quiz.description = payload.description
        if payload.time_limit:
            quiz.time_limit = payload.time_limit
        if payload.user:
            quiz.user_id = payload.user
        quiz.save()
        
        # modules ni yangilash
        if payload.modules:
            quiz.modules.clear()
            for module_id in payload.modules:
                module = MyModules.objects.get(id=module_id)
                quiz.modules.add(module)
        
        return {
            "id": quiz.id,
            "title": quiz.title,
            "slug": quiz.slug,
            "description": quiz.description,
            "modules": [module.id for module in quiz.modules.all()],
            "time_limit": quiz.time_limit,
            "user": quiz.user.id,
            "created_at": quiz.created_at,
            "updated_at": quiz.updated_at,
        }
    except Exception as e:
        raise HttpError(400, f"Quizni yangilashda xato: {str(e)}")

# Delete a quiz
@quize_router.delete("delete/{quiz_id}", auth=[IsSuperuser(), IsStaff()])
def quize_delete(request, quiz_id: int):
    try:
        quiz = Quiz.objects.filter(id=quiz_id).first()
        if not quiz:
            raise HttpError(404, "Quiz not found")
        quiz.delete()
        return {"success": True}
    except Exception as e:
        raise HttpError(400, f"Quizni o'chirishda xato: {str(e)}")

# Search quizzes by title and description
@quize_router.get("/search/", response=List[QuizSchemaList], auth=[IsSuperuser(), IsStaff()])
def quize_search(
    request,
    search: str = QueryEx(..., min_length=3, description="Quizni sarlavha yoki tavsif bo'yicha qidirish (kamida 3 belgi)"),
    limit: int = QueryEx(10, ge=1, le=100, description="Qaytariladigan quizlar soni (1 dan 100 gacha)"),
):
    try:
        quizzes = Quiz.objects.filter(
            title__icontains=search,
            description__icontains=search
        )[:limit]
        return [
            {
                "id": quiz.id,
                "title": quiz.title,
                "slug": quiz.slug,
                "description": quiz.description,
                "modules": [module.id for module in quiz.modules.all()],
                "time_limit": quiz.time_limit,
                "user": quiz.user.id,
                "created_at": quiz.created_at,
                "updated_at": quiz.updated_at,
            }
            for quiz in quizzes
        ]
    except Exception as e:
        raise HttpError(400, f"Qidiruvda xato: {str(e)}")