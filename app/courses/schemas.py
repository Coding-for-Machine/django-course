from ninja import ModelSchema
from pydantic import BaseModel
from typing import List, Optional

from .models import Course

class CourseResponse(BaseModel):
    title: str
    slug: str
    price: int
    description: str
    thumbnail: str
    lesson_count: Optional[int] = 0  # Default to 0 if None
    trailer: Optional[str] = None

    class Config:
        orm_mode = True

class CoursesListResponse(BaseModel):
    all: List[CourseResponse]
    enrolled: List[CourseResponse]

    class Config:
        orm_mode = True


class LessonStatusSchima(BaseModel):
    is_completed: bool
    progress: str

# Lesson Schema
class LessonSchema(BaseModel):
    slug: str
    title: str
    type: str  # 'lecture' or 'lab'
    locked: bool
    preview: bool
    lesson_status: List[LessonStatusSchima]

    class Config:
        orm_mode = True

# Module Schema
class ModuleSchema(BaseModel):
    slug: str
    title: str
    description: Optional[str] = None
    lessons: List[LessonSchema]

    class Config:
        orm_mode = True


# Course Schema
class CourseSchema(BaseModel):
    slug: str
    title: str
    price: int
    enrolled: bool
    description: str
    trailer: str
    thumbnail: str
    lesson_count: int
    modules: List[ModuleSchema]
    group_link: Optional[str] = None

    class Config:
        orm_mode = True
# course list 
# class CourseSchema(ModelSchema):
#     class Config:
#         model = Course
#         fields = "__all__"
# # course Create
# class CourseCreateSchema(BaseModel):
#     title: str
#     price: int
#     description: str
#     thumbnail: str
#     trailer: str | None = None
#     unlisted: bool = False


