from ninja import Router
from django_redis import get_redis_connection
from django.shortcuts import get_object_or_404
from django.http import HttpRequest
import json

from lessons.models import Lesson
from .models import Course, Enrollment, MyModules
from .schemas import CoursesListResponse, CourseSchema
from userstatus.models import UserLessonStatus

from users.api_auth import api_auth_user_or_annon

api_course = Router()


# Kurslar ro'yxatini olish va JSON formatda qaytarish
@api_course.get("/courses/", response=CoursesListResponse, auth=api_auth_user_or_annon)
def get_courses(request: HttpRequest):
    if not request.user.is_authenticated:
        pass
    else:
        redis_conn = get_redis_connection("default")  # Redis ulanishini olish
        user_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', 'unknown_ip'))
        cache_key = f"user_courses_cache_{user_ip}"  # Har bir foydalanuvchi uchun alohida cache
        cached_data = redis_conn.get(cache_key)
        if cached_data:
            return json.loads(cached_data)  # Agar cache mavjud bo‘lsa, JSON qilib qaytaramiz

        # Foydalanuvchi ID sini olish
        user_id = request.user.id if request.user.is_authenticated else None
        courses = Course.objects.all()

        enrolled_courses = []

        # Foydalanuvchining kursga yozilganlarini olish
        if user_id:
            enrollments = Enrollment.objects.filter(user_id=user_id, is_paid=True)
            enrolled_courses = [enrollment.course for enrollment in enrollments]

        # Ro'yxatdan o'tmagan kurslar
        all_courses = [
            {
                "title": course.title,
                "slug": course.slug,
                "price": course.price,
                "description": course.description,
                "thumbnail": course.thumbnail,
                "lesson_count": course.lesson_count if course.lesson_count is not None else 0,
                "trailer": course.trailer,
                "unlisted": course.unlisted
            }
            for course in courses if course not in enrolled_courses
        ]

        # Ro‘yxatdan o‘tgan kurslar
        enrolled = [
            {
                "title": course.title,
                "slug": course.slug,
                "price": course.price,
                "description": course.description,
                "thumbnail": course.thumbnail,
                "lesson_count": course.lesson_count if course.lesson_count is not None else 0,
                "trailer": course.trailer,
                "unlisted": course.unlisted
            }
            for course in enrolled_courses
        ]

        response_data = {
            "all": all_courses,  
            "enrolled": enrolled,  
        }

        # Redis'ga 5 daqiqaga cache saqlash
        redis_conn.setex(cache_key, 300, json.dumps(response_data))

        return response_data


@api_course.get("/courses/{slug}", response={200: dict, 404: str}, auth=api_auth_user_or_annon)
def get_course_by_slug(request: HttpRequest, slug: str):
    redis_conn = get_redis_connection("default")
    user_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', 'unknown_ip'))
    cache_key = f"user_course_detail_cache_{user_ip}_{slug}"  # IP va kurs slug'iga ko‘ra cache

    cached_data = redis_conn.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    course = get_object_or_404(Course, slug=slug)
    user_id = request.user.id if request.user.is_authenticated else None
    enrolled_courses = []

    if user_id:
        enrollments = Enrollment.objects.filter(user_id=user_id)
        enrolled_courses = [enrollment.course for enrollment in enrollments]

    enrolled = course in enrolled_courses
    modules = MyModules.objects.filter(course=course)

    course_data = {
        "courses_and_lesson": [{
            "slug": course.slug,
            "title": course.title,
            "price": course.price,
            "description": course.description,
            "trailer": course.trailer,
            "thumbnail": course.thumbnail,
            "lesson_count": course.lesson_count if course.lesson_count is not None else 0,
            "modules": [
                {
                    "slug": module.slug,
                    "title": module.title,
                    "description": module.description,
                    "lessons": [{
                            "slug": lesson.slug,
                            "title": lesson.title,
                            "type": lesson.lesson_type,
                            "locked": lesson.locked,
                            "preview": lesson.preview,
                            "lesson_status": [
                                {
                                    "is_comlact": status.is_completed,
                                    "progress": status.progress,
                                }
                                for status in UserLessonStatus.objects.filter(lesson=lesson, user=user_id)
                            ]
                        }
                        for lesson in Lesson.objects.filter(module=module)
                    ],
                   
                }
                for module in modules
            ],
        }],
        "enrolled": enrolled,
        "group_link": None  
    }

    # Redis'ga 5 daqiqaga cache qilish
    redis_conn.setex(cache_key, 300, json.dumps(course_data))

    return course_data

# create courses
# @api_course.post("/courses", response=CourseSchema)
# def create_course(request, payload: CourseCreateSchema):
#     course = Course.objects.create(**payload.dict())
#     return course

# #  delete course
# @api_course.delete("/courses/{course_id}")
# def delete_course(request, course_id: int):
#     course = Course.objects.get(id=course_id)
#     course.delete()
#     return {"message": "Course deleted"}