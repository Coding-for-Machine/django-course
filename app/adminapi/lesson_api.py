from ninja import Router
from ninja.errors import HttpError
from lessons.models import Lesson
from typing import List
from pydantic import BaseModel

lesson_router_api = Router()

# ----------------------- lesson schemas ---------------------
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
    module: int  # module ID ni qabul qiladi
    title: str
    lesson_type: bool  # faqat bitta lesson_type bo'lishi kerak
    locked: bool
    preview: bool
    user: int  # user ID ni qabul qiladi

# ----------------------- crud schemas ---------------------

# lesson list api - http method get
@lesson_router_api.get("/", response=List[LessonList])
def lesson_list_api(request):
    lessons = Lesson.objects.filter(is_active=True)
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
        for lesson in lessons
    ]

# lesson ni o'qish get slug bo'yicha
@lesson_router_api.get("/{slug}", response=LessonList)
def lesson_detail_api(request, slug: str):
    try:
        lesson = Lesson.objects.get(slug=slug, is_active=True)
        return {
            "id": lesson.id,
            "module": lesson.module.id,
            "title": lesson.title,
            "slug": lesson.slug,
            "lesson_type": lesson.lesson_type,
            "locked": lesson.locked,
            "preview": lesson.preview,
            "user": lesson.user.id,
        }
    except Lesson.DoesNotExist:
        raise HttpError(404, "Lesson topilmadi!")
    except Exception as e:
        raise HttpError(500, f"Xato yuz berdi: {str(e)}")

# lesson ga qo'shish - create lesson
@lesson_router_api.post("/create/", response=LessonList)
def lesson_create(request, data: LessonCreate):
    try:
        lesson = Lesson.objects.create(
            module_id=data.module,  # module_id orqali bog'lash
            title=data.title,
            lesson_type=data.lesson_type,
            locked=data.locked,
            preview=data.preview,
            user_id=data.user,  # user_id orqali bog'lash
        )
        return {
            "id": lesson.id,
            "module": lesson.module.id,
            "title": lesson.title,
            "slug": lesson.slug,
            "lesson_type": lesson.lesson_type,
            "locked": lesson.locked,
            "preview": lesson.preview,
            "user": lesson.user.id,
        }
    except Exception as e:
        raise HttpError(400, f"Lesson yaratishda xato: {str(e)}")

# lesson ni update qilish uchun
@lesson_router_api.put("/update/{slug}", response=LessonList)
def lesson_update_api(request, slug: str, data: LessonCreate):
    try:
        lesson = Lesson.objects.get(slug=slug, is_active=True)
        for key, value in data.dict().items():  # .items() to'g'ri
            setattr(lesson, key, value)
        lesson.save()
        return {
            "id": lesson.id,
            "module": lesson.module.id,
            "title": lesson.title,
            "slug": lesson.slug,
            "lesson_type": lesson.lesson_type,
            "locked": lesson.locked,
            "preview": lesson.preview,
            "user": lesson.user.id,
        }
    except Lesson.DoesNotExist:
        raise HttpError(404, "Lesson topilmadi!")
    except Exception as e:
        raise HttpError(400, f"Lessonni yangilashda xato: {str(e)}")

# lesson ni o'chirish
@lesson_router_api.delete("/delete/{slug}")
def lesson_delete_api(request, slug: str):
    try:
        lesson = Lesson.objects.get(slug=slug, is_active=True)
        lesson.delete()
        return {"success": True, "message": "Lesson muvaffaqiyatli o'chirildi"}
    except Lesson.DoesNotExist:
        raise HttpError(404, "Lesson topilmadi!")
    except Exception as e:
        raise HttpError(400, f"Lessonni o'chirishda xato: {str(e)}")