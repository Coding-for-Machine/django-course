from ninja import Router
from pydantic import BaseModel
from typing import List, Optional
from django.http import Http404
from courses.models import Course

course_api_router = Router()

# --------------------------------schema course ------------------------
class CourseList(BaseModel):
    id: int
    title: str
    slug: str
    price: int
    description: str
    thumbnail: str
    lesson_count: int
    trailer: str
    unlisted: bool

class CourseCreate(BaseModel):
    title: str
    price: int
    description: str
    thumbnail: str
    lesson_count: int
    trailer: str
    unlisted: bool

# ----------------------------course api functions ----------------------

# course get api -- admin uchun
@course_api_router.get('courses-get/', response=List[CourseList])
def course_api_get_admin(request):
    courses = Course.objects.all().filter(is_active=True)
    return [
        {
            "id": course.id,
            "title": course.title,
            "slug": course.slug,
            "price": course.price,
            "description": course.description,
            "thumbnail": course.thumbnail,
            "lesson_count": course.lesson_count,
            "trailer": course.trailer,
            "unlisted": course.unlisted
        }
        for course in courses
    ]

# course get - slug orqali
@course_api_router.get('course-get/{course_slug}/', response=CourseList)
def course_api_get_slug_admin(request, course_slug: str):
    try:
        course = Course.objects.get(slug=course_slug)
        return {
            "id": course.id,
            "title": course.title,
            "slug": course.slug,
            "price": course.price,
            "description": course.description,
            "thumbnail": course.thumbnail,
            "lesson_count": course.lesson_count,
            "trailer": course.trailer,
            "unlisted": course.unlisted
        }
    except Course.DoesNotExist:
        raise Http404("Darslik topilmadi!")

# course post api -- create courses
@course_api_router.post('course-create', response=CourseList)
def course_api_post_admin(request, data: CourseCreate):
    course = Course.objects.create(**data.dict())
    return {
        "id": course.id,
        "title": course.title,
        "slug": course.slug,
        "price": course.price,
        "description": course.description,
        "thumbnail": course.thumbnail,
        "lesson_count": course.lesson_count,
        "trailer": course.trailer,
        "unlisted": course.unlisted
    }

# course put api - course ni o'zgartirish
@course_api_router.put("course-update/{course_slug}/", response=CourseList)
def course_api_put_admin(request, course_slug: str, data: CourseCreate):
    try:
        course = Course.objects.get(slug=course_slug)
        for key, value in data.dict().items():
            setattr(course, key, value)
        course.save()
        return {
            "id": course.id,
            "title": course.title,
            "slug": course.slug,
            "price": course.price,
            "description": course.description,
            "thumbnail": course.thumbnail,
            "lesson_count": course.lesson_count,
            "trailer": course.trailer,
            "unlisted": course.unlisted
        }
    except Course.DoesNotExist:
        raise Http404("Darslik topilmadi!")

# course delete api - course ni o'chirish
@course_api_router.delete("course-delete/{course_slug}/")
def course_api_delete_admin(request, course_slug: str):
    try:
        course = Course.objects.get(slug=course_slug)
        course.delete()
        return {"success": True, "message": "Course deleted successfully"}
    except Course.DoesNotExist:
        raise Http404("Darslik topilmadi!")