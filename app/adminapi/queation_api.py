from ninja import Router
from pydantic import BaseModel
from typing import Any, List, Optional
from datetime import datetime
from savollar.models import Question

class QuestionList(BaseModel):
    id: int
    content_type: int
    object_id: int
    description: str
    user: List[Any]
    created_at: datetime
    updated_at: datetime


class QuestionsCreate(BaseModel):
    content_type: List[Any]
    object_id: int
    description: str
    user: List[Any]
    created_at: datetime
    updated_at: datetime

question_router = Router()

# get question
@question_router.get("/", response=List[QuestionList])
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

# get question
@question_router.get("/", response=List[QuestionList])
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
