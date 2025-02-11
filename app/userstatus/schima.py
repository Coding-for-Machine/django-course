from pydantic import BaseModel
from typing import List, Dict, Optional, Any


class UserLessonStatusSchames(BaseModel):
    id: str
    users: List
    lesson: List
    is_completed: bool
    progress: int


