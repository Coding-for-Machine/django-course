from ninja import Router
from pydantic import BaseModel
from typing import Any, List, Optional
from datetime import datetime

class Question(BaseModel):
    id: int
    content_type: List[Any]
    object_id: int
    description: str
    user: List[Any]
    created_at: datetime
    updated_at: datetime
