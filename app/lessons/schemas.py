from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LessonSchema(BaseModel):
    module: str  # You can use the module title or module ID if needed
    title: str
    slug: str
    lesson_type: str  # Either 'lecture' or 'lab'
    locked: bool
    preview: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # To enable compatibility with ORM models (Django Models)

# # Optional: Create an input schema for creating/updating lessons
# class LessonCreateSchema(BaseModel):
#     module: str
#     title: str
#     slug: str
#     lesson_type: str
#     locked: bool = False
#     preview: bool = False

#     class Config:
#         orm_mode = True

# class LessonUpdateSchema(BaseModel):
#     title: Optional[str] = None
#     slug: Optional[str] = None
#     lesson_type: Optional[str] = None
#     locked: Optional[bool] = None
#     preview: Optional[bool] = None

#     class Config:
#         orm_mode = True
