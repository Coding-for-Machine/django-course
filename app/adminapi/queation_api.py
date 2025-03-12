from ninja import Router, Query
from ninja.errors import HttpError
from django.http import HttpResponse
from pydantic import BaseModel
from typing import Any, List, Optional
from datetime import datetime
from django.db.models import Q
from savollar.models import Question

from .auth_permission import IsStaff, IsSuperuser

class QuestionList(BaseModel):
    id: int
    content_type: int
    object_id: int
    description: str
    user: int
    created_at: datetime
    updated_at: datetime

class QuestionsCreate(BaseModel):
    content_type: int
    object_id: int
    description: str
    user: int

question_router = Router()

# get question
@question_router.get("/", response=List[QuestionList], auth=[IsStaff(), IsSuperuser()])
def question_get(request):
    return [
        {
            "id": q.id,
            "content_type": q.content_type,
            "object_id": q.object_id,
            "description": q.description,
            "user": q.user.id,
            "created_at": q.created_at,
            "updated_at": q.updated_at,
        }
        for q in Question.objects.all()
    ]

# get id questions
@question_router.get("/{id}/", response=QuestionList, auth=[IsStaff(), IsSuperuser()])
def question_id_get(request, id: int):
    try:
        q = Question.objects.get(id=id)
        return {
            "id": q.id,
            "content_type": q.content_type,
            "object_id": q.object_id,
            "description": q.description,
            "user": q.user.id,
            "created_at": q.created_at,
            "updated_at": q.updated_at,
        }
    except Question.DoesNotExist:
        raise HttpError(404, "topilmadi!")
    except Exception as e:
        raise HttpError(500, f"Nimadur xato ketti!, {str(e)}")

@question_router.post("/create/", response=QuestionList, auth=[IsStaff(), IsSuperuser()])
def question_create(request, data: QuestionsCreate):
    try:
        q = Question.objects.create(**data.dict())
        return {
            "id": q.id,
            "content_type": q.content_type,
            "object_id": q.object_id,
            "description": q.description,
            "user": q.user.id,
            "created_at": q.created_at,
            "updated_at": q.updated_at,
        }
    except Exception as e:
        raise HttpError(500, f"Nimadur xato ketti!, {str(e)}")

@question_router.put("/{id}/", response=QuestionList, auth=[IsStaff(), IsSuperuser()])
def question_update(request, id: int, data: QuestionsCreate):
    try:
        q = Question.objects.get(id=id)
        for key, value in data.dict().items():
            setattr(q, key, value)
        q.save()
        return {
            "id": q.id,
            "content_type": q.content_type,
            "object_id": q.object_id,
            "description": q.description,
            "user": q.user.id,
            "created_at": q.created_at,
            "updated_at": q.updated_at,
        }
    except Question.DoesNotExist:
        raise HttpError(404, "topilmadi!")
    except Exception as e:
        raise HttpError(500, f"Nimadur xato ketti!, {str(e)}")

@question_router.delete("/{id}/", response=dict, auth=[IsStaff(), IsSuperuser()])
def question_delete(request, id: int):
    try:
        q = Question.objects.get(id=id)
        q.delete()
        return {"success": True, "message": "Ma'lumot muvaffaqiyatli o'chirildi"}
    except Question.DoesNotExist:
        raise HttpError(404, "topilmadi!")
    except Exception as e:
        raise HttpError(500, f"Nimadur xato ketti!, {str(e)}")
    

# querys
class QuestionFilter(BaseModel):
    title: Optional[str] = None
    difficulty: Optional[str] = None
    tags: Optional[List[str]] = None
    created_year: Optional[int] = None
    created_month: Optional[int] = None
    created_day: Optional[int] = None

@question_router.get("/search/", response=List[QuestionList])
def search_questions(request, filters: QuestionFilter = Query(...)):
    query = Q()

    # Filter by title OR difficulty
    if filters.title:
        query |= Q(title__icontains=filters.title)
    if filters.difficulty:
        query |= Q(difficulty=filters.difficulty)

    # Filter by tags (AND sharti)
    if filters.tags:
        query &= Q(tags__name__in=filters.tags)

    # Filter by creation date (yil, oy, kun)
    if filters.created_year:
        query &= Q(created_at__year=filters.created_year)
    if filters.created_month:
        query &= Q(created_at__month=filters.created_month)
    if filters.created_day:
        query &= Q(created_at__day=filters.created_day)

    questions = Question.objects.filter(query).distinct()
    return [
        {
            "id": q.id,
            "title": q.title,
            "description": q.description,
            "difficulty": q.difficulty,
            "created_at": q.created_at,
            "updated_at": q.updated_at,
            "tags": [tag.name for tag in q.tags.all()],
        }
        for q in questions
    ]