from django.shortcuts import get_object_or_404
from ninja import Router
from pydantic import BaseModel
from typing import List
from django.http import Http404
from users.models import MyUser
from courses.models import Course
from .auth_permission import *

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
    user: int
    unlisted: bool


class CourseCreate(BaseModel):
    title: str
    price: int
    description: str
    thumbnail: str
    lesson_count: int
    trailer: str
    unlisted: bool
    slug: str  # Agar kerak bo'lsa
    user: int


# ----------------------------course api functions ----------------------

# course get api -- admin uchun
@course_api_router.get('courses-get/', response=List[CourseList], auth=[IsSuperuser()])
def course_api_get_admin(request):
    courses = Course.objects.filter(is_active=True)
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
            "unlisted": course.unlisted,
            "user": course.user.id
        }
        for course in courses
    ]

# course get - slug orqali
@course_api_router.get('course-get/{course_slug}/', response=CourseList, auth=[IsSuperuser(), IsStaff(), IsInGroup("Teacher")])
def course_api_get_slug_admin(request, course_slug: str):
    try:
        if request.user.is_staff or request.user.is_superuser:
            course = Course.objects.get(slug=course_slug)
        else:
            course = Course.objects.get(user=request.user, slug=course_slug)
        return {
            "id": course.id,
            "title": course.title,
            "slug": course.slug,
            "price": course.price,
            "description": course.description,
            "thumbnail": course.thumbnail,
            "lesson_count": course.lesson_count,
            "trailer": course.trailer,
            "unlisted": course.unlisted,
            "user": course.user.id

        }
    except Course.DoesNotExist:
        raise Http404("Darslik topilmadi!")

# course post api -- create courses
@course_api_router.post('course-create', response=CourseList, auth=[IsSuperuser(), IsStaff(), IsInGroup("Teacher")])
def course_api_post_admin(request, data: CourseCreate):
    
    user = get_object_or_404(MyUser, id=data.user)  # User obyektini olish
    
    course = Course.objects.create(
        title=data.title,
        slug=data.slug,
        price=data.price,
        description=data.description,
        thumbnail=data.thumbnail,
        lesson_count=data.lesson_count,
        trailer=data.trailer,
        unlisted=data.unlisted,
        user=user  # MyUser obyektini qo‘shish
    )

    return {
        "id": course.id,
        "title": course.title,
        "slug": course.slug,
        "price": course.price,
        "description": course.description,
        "thumbnail": course.thumbnail,
        "lesson_count": course.lesson_count,
        "trailer": course.trailer,
        "unlisted": course.unlisted,
        "user": course.user.id
    }

# course put api - course ni o'zgartirish
@course_api_router.put("course-update/{course_slug}/", response=CourseList, auth=[IsSuperuser(), IsStaff(), IsInGroup("Teacher")])
def course_api_put_admin(request, course_slug: str, data: CourseCreate):
    try:
        request_user = request.user
        if request_user.is_staff or request_user.is_superuser:
            course = Course.objects.get(slug=course_slug)
        elif Course.objects.filter(user=request_user, slug=course_slug).exists():
            course = Course.objects.get(user=request_user, slug=course_slug)
        else:
            return {"error": "sizning darsliginggiz emas!"}

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
            "unlisted": course.unlisted,
            "user": course.user.id

        }
    except Course.DoesNotExist:
        raise Http404("Darslik topilmadi!")

# course delete api - course ni o'chirish
@course_api_router.delete("course-delete/{course_slug}/", auth=[IsSuperuser(), IsStaff(), IsInGroup("Teacher")])
def course_api_delete_admin(request, course_slug: str):
    try:
        request_user = request.user
        if request_user.is_staff or request_user.is_superuser:
            course = Course.objects.get(slug=course_slug)
        else:
            course = Course.objects.get(user=request_user, slug=course_slug)
        course.delete()
        return {"success": True, "message": "Course deleted successfully"}
    except Course.DoesNotExist:
        raise Http404("Darslik topilmadi!")