from ninja import NinjaAPI
from django.shortcuts import get_object_or_404

from lessons.models import Lesson
from .models import Course, Enrollment, Module
from .schemas import CourseSchema, CoursesListResponse


api = NinjaAPI()

# Kurslar ro'yxatini olish va JSON formatda qaytarish
@api.get("/courses/", response=CoursesListResponse)
def get_courses(request):
    # Foydalanuvchining ID raqamini olish
    user_id = request.user.id if request.user.is_authenticated else None
    courses = Course.objects.all()

    enrolled_courses = []

    # Foydalanuvchining kursga ro'yxatdan o'tgan kurslarini olish
    if user_id:
        enrollments = Enrollment.objects.filter(user_id=user_id)
        enrolled_courses = [enrollment.course for enrollment in enrollments]

    # Course ro'yxatini yaratish
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
        for course in courses if course not in enrolled_courses  # Only include courses the user is not enrolled in
    ]

    # Enrolled course list for authenticated user
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

    return {
        "all": all_courses,  # All courses excluding the ones user is enrolled in
        "enrolled": enrolled,  # Enrolled courses for the authenticated user
    }


@api.get("/courses/{slug}", response={200: dict, 404: str})
def get_course_by_slug(request, slug: str):
    course = get_object_or_404(Course, slug=slug)
    user_id = request.user.id if request.user.is_authenticated else None
    model = []
    if user_id:
        # Fetch the courses the user is enrolled in
        enrollments = Enrollment.objects.filter(user_id=user_id)
        model = [enrollment.course for enrollment in enrollments]

    # Check if the user is enrolled in this course
    enrolled = course in model
    
    # Fetch the related modules and lessons for the course
    modules = Module.objects.filter(course=course)
    
    course_data = {
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
                "lessons": [
                    {
                        "slug": lesson.slug,
                        "title": lesson.title,
                        "type": lesson.lesson_type,
                        "locked": lesson.locked,
                        "preview": lesson.preview,
                    }
                    for lesson in Lesson.objects.filter(module=module)
                ]
            }
            for module in modules
        ],
        "enrolled": enrolled,  # If the user is enrolled in this course
        "group_link": None  # Adjust as necessary
    }

    return course_data
