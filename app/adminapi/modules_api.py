from ninja import Router
from ninja.errors import HttpError
from pydantic import BaseModel
from datetime import datetime
from typing import List
from courses.models import MyModules
from django.http import Http404
from .auth_permission import IsSuperuser, IsStaff

api_module_router = Router()

# -------------------modules api schemas----------------------------------------

class ModuleList(BaseModel):
    id: int
    course: int
    title: str
    slug: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

class ModuleCreate(BaseModel):
    course: int
    title: str
    description: str
    is_active: bool = True  # Default qiymat qo'shildi

# -------------------modules api CRUD-------------------------------------------

@api_module_router.get("/module-get/", response=List[ModuleList], auth=[IsSuperuser(), IsStaff()])
def get_module_api(request):
    modules = MyModules.objects.filter(is_active=True)
    return [
        {
            "id": module.id,
            "course": module.course.id,  # course_id emas, course deb nomlandi
            "title": module.title,
            "slug": module.slug,
            "description": module.description,
            "is_active": module.is_active,
            "created_at": module.created_at,
            "updated_at": module.updated_at,
        }
        for module in modules
    ]

@api_module_router.get("/get/{slug}/", response=ModuleList, auth=[IsSuperuser(), IsStaff()])
def get_slug_module_api(request, slug: str):
    try:
        module = MyModules.objects.get(slug=slug, is_active=True)  # get() dan foydalanildi
        return {
            "id": module.id,
            "course": module.course.id,  # course_id emas, course deb nomlandi
            "title": module.title,
            "slug": module.slug,
            "description": module.description,
            "is_active": module.is_active,
            "created_at": module.created_at,
            "updated_at": module.updated_at,
        }
    except MyModules.DoesNotExist:  # DoesNotExist ni () siz ishlatildi
        raise Http404("module topilmadi 404")
    
@api_module_router.post("/create/", response=ModuleList, auth=[IsSuperuser(), IsStaff()])
def post_module_api(request, data: ModuleCreate):
    try:
        from courses.models import Course  # Course modelini import qilish

        # Course obyektini topish
        course_instance = Course.objects.get(id=data.course)

        # MyModules obyektini yaratish
        module = MyModules.objects.create(
            course=course_instance,  # Course obyektini berish
            title=data.title,
            description=data.description,
            is_active=data.is_active,
        )

        return {
            "id": module.id,
            "course": module.course.id,  # course_id emas, course deb nomlandi
            "title": module.title,
            "slug": module.slug,
            "description": module.description,
            "is_active": module.is_active,
            "created_at": module.created_at,
            "updated_at": module.updated_at,
        }
    except Course.DoesNotExist:
        raise HttpError(404, "Course topilmadi")
    except Exception as e:
        raise HttpError(400, f"Bad Request: {str(e)}")
    
# course update 
@api_module_router.put("update/", response=ModuleList, auth=[IsSuperuser(), IsStaff()])
def update_module_api(request, slug: str, data: ModuleCreate):
    try:
        module = MyModules.objects.get(slug=slug, is_active=True)
        for key, value in data.dict().items():
            setattr(module, key, value)
        module.save()
        return {
            "id": module.id,
            "course": module.course.id,  # course_id emas, course deb nomlandi
            "title": module.title,
            "slug": module.slug,
            "description": module.description,
            "is_active": module.is_active,
            "created_at": module.created_at,
            "updated_at": module.updated_at,
        }
    except Exception as e:
        raise HttpError(400, f"module topilmadi!, {str(e)}")