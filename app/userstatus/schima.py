from pydantic import BaseModel, EmailStr
from typing import List, Dict, Optional, Any
from datetime import datetime

class UserLessonStatusSchames(BaseModel):
    id: str
    users: List
    lesson: List
    is_completed: bool
    progress: int


class UserSchemas(BaseModel):
    id: int
    email: EmailStr

class UserActivityDailyLists(BaseModel):
    user: UserSchemas
    date: datetime
    