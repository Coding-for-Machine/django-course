from ninja import Router
from ninja.errors import HttpError
from lessons.models import  Lesson

lesson_router_api = Router()

# ----------------------- lesson schemas ---------------------
from pydantic import BaseModel
from typing import List

class LessonList(BaseModel):
    id: int
    module: int
    title: str
    slug: str
    lesson_type: bool
    locked: bool
    preview: bool
    user: int

class LessonCreate(BaseModel):
    module: id
    title: str
    lesson_type: int
    lesson_type: bool
    locked: bool
    preview: bool
    user: int
# ----------------------- crud schemas ---------------------

# lesson list api - http method get
@lesson_router_api.get("/", response=List[LessonList])
def lesson_list_api(request):
    return [
        {
            "id": lesson.id,
            "module": lesson.module.id,
            "title": lesson.title,
            "slug": lesson.slug,
            "lesson_type": lesson.lesson_type,
            "locked": lesson.locked,
            "preview": lesson.preview,
            "user": lesson.user.id,
        }
        for lesson in Lesson.objects.all().filter(is_active=True)
    ]
# lesson ni o'qish get slug bo'yicha
@lesson_router_api.get("/{slug}", response=LessonList)
def lesson_list_api(request, slug: str):
    try:
        lesson = Lesson.objects.get(slug=slug, is_active=True)
        return [
            {
                "id": lesson.id,
                "module": lesson.module.id,
                "title": lesson.title,
                "slug": lesson.slug,
                "lesson_type": lesson.lesson_type,
                "locked": lesson.locked,
                "preview": lesson.preview,
                "user": lesson.user.id,
            }
        ]
    except Exception as e:
        raise HttpError(404, f"lesson object slug mos emas! {str(e)}")

# lesson ga qo'shsish -create lesson
@lesson_router_api.post("create/", response=LessonList)
def lesson_create(request, data: LessonCreate):
    try:
        lesson = Lesson.objects.create(**data.dict())
        return [
            {
                "id": lesson.id,
                "module": lesson.module.id,
                "title": lesson.title,
                "slug": lesson.slug,
                "lesson_type": lesson.lesson_type,
                "locked": lesson.locked,
                "preview": lesson.preview,
                "user": lesson.user.id,
            }
        ]
    except Exception as e:
        raise HttpError(f"Leson kiritilmadi!, {str(e)}")
    


# lesson ni update qilish uchin
@lesson_router_api.put("update/", response=LessonList)
def lesson_update_api(request, slug: str, data: LessonCreate):
    try:
        lesson = Lesson.objects.get(slug=slug, is_active=True)
        for key, value in data.dict.item():
            setattr(lesson, key, value)
        lesson.save()
        return [
            {
                "id": lesson.id,
                "module": lesson.module.id,
                "title": lesson.title,
                "slug": lesson.slug,
                "lesson_type": lesson.lesson_type,
                "locked": lesson.locked,
                "preview": lesson.preview,
                "user": lesson.user.id,
            }
        ]
    except Exception as e:
        raise HttpError(403, f"Lessonni o'zgartirishda xato ketti!, {str(e)}")
    
# lesson ni uchirish 
@lesson_router_api.delete("delete/", response=LessonList)
def lesson_delete_api(request, slug: str):
    try:
        lesson = Lesson.objects.get(slug=slug, is_active=True)
        lesson.delete()
        return [
            {
                "id": lesson.id,
                "module": lesson.module.id,
                "title": lesson.title,
                "slug": lesson.slug,
                "lesson_type": lesson.lesson_type,
                "locked": lesson.locked,
                "preview": lesson.preview,
                "user": lesson.user.id,
            }
        ]
    except Exception as e:
        raise HttpError(404, f"lesson topilmadi!, {str(e)}")
