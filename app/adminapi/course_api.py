from django.shortcuts import get_object_or_404
from ninja import Router
from pydantic import BaseModel
from typing import List
from django.http import Http404
from users.models import MyUser
from courses.models import Course
from .auth_permission import IsInGroup, IsSuperuser, IsStaff

course_api_router = Router()

# --------------------------------schema course ------------------------
class UserSchema(BaseModel):
    id: int
    email: str

class CourseList(BaseModel):
    id: int
    title: str
    slug: str
    price: int
    description: str
    thumbnail: str
    lesson_count: int
    trailer: str
    user: UserSchema
    unlisted: bool
    created_at: str
    updated_at: str

class CourseCreate(BaseModel):
    title: str
    price: int
    description: str
    thumbnail: str
    lesson_count: int
    trailer: str

# ----------------------------course api functions ----------------------

def serialize_course(course: Course):
    return {
        "id": course.id,
        "title": course.title,
        "slug": course.slug,
        "price": course.price,
        "description": course.description,
        "thumbnail": course.thumbnail,
        "lesson_count": course.lesson_count,
        "trailer": course.trailer,
        "unlisted": course.is_active,
        "created_at": course.created_at.isoformat(),
        "updated_at": course.updated_at.isoformat(),
        "user": {
            "id": course.user.id,
            "email": course.user.email
        }
    }

# course get api -- admin uchun
@course_api_router.get('courses-get/', response=List[CourseList], auth=[IsSuperuser(), IsInGroup("Teacher"), IsStaff()])
def course_api_get_admin(request):
    courses = Course.objects.filter(is_active=True)
    return [serialize_course(course) for course in courses]

# course get - slug orqali
@course_api_router.get('course-get/{course_slug}/', response=CourseList, auth=[IsSuperuser(), IsStaff(), IsInGroup("Teacher")])
def course_api_get_slug_admin(request, course_slug: str):
    course = get_object_or_404(Course, slug=course_slug)
    return serialize_course(course)

# course post api -- create courses
@course_api_router.post('course-create/', response=CourseList, auth=[IsSuperuser(), IsStaff(), IsInGroup("Teacher")])
def course_api_post_admin(request, data: CourseCreate):
    user = get_object_or_404(MyUser, id=request.user.id)
    course = Course.objects.create(
        title=data.title,
        price=data.price,
        description=data.description,
        thumbnail=data.thumbnail,
        lesson_count=data.lesson_count,
        trailer=data.trailer,
        user=user
    )
    return serialize_course(course)

# course put api - course ni o'zgartirish
@course_api_router.put("course-update/{course_slug}/", response=CourseList, auth=[IsSuperuser(), IsStaff(), IsInGroup("Teacher")])
def course_api_put_admin(request, course_slug: str, data: CourseCreate):
    course = get_object_or_404(Course, slug=course_slug)
    for key, value in data.dict().items():
        setattr(course, key, value)
    course.save()
    return serialize_course(course)

# course delete api - course ni o'chirish
@course_api_router.delete("course-delete/{course_slug}/", auth=[IsSuperuser(), IsStaff(), IsInGroup("Teacher")])
def course_api_delete_admin(request, course_slug: str):
    course = get_object_or_404(Course, slug=course_slug)
    course.delete()
    return {"success": True, "message": "Course deleted successfully"}
