from ninja import Router
from ninja.errors import HttpError
from lessons.models import Function
from .auth_permission import IsSuperuser, IsStaff

# ------------------ schemas function-------------------------
from pydantic import BaseModel
from datetime import datetime
from typing import List

class FunctionList(BaseModel):
    id: int
    language: int
    problem: int
    function: str
    user: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

class FunctionCreate(BaseModel):
    language: int
    problem: int
    function: str
    user: int
    is_active: bool
    
# ------------------ crud function admin uchin----------------

function_router_api = Router()
#  get func 
@function_router_api.get("/", response=List[FunctionList], auth=[IsSuperuser(), IsStaff()])
def func_get(request):
    return [
        {
            "id": func.id,
            "language": func.language,
            "problem": func.problem,
            "function": func.function,
            "user": func.user,
            "is_active": func.is_active,
            "created_at": func.created_at,
            "updated_at": func.updated_at
        }
        for func in Function.objects.all()
    ]


@function_router_api.get("{id}/", response=FunctionList, auth=[IsSuperuser(), IsStaff()])
def func_get(request, id: int):
    try:
        func = Function.objects.get(id=id)
        return {
                "id": func.id,
                "language": func.language,
                "problem": func.problem,
                "function": func.function,
                "user": func.user,
                "is_active": func.is_active,
                "created_at": func.created_at,
                "updated_at": func.updated_at
            }
    except Exception as e:
        raise HttpError(404, "Topilmadi!")
    
@function_router_api.post("create/", response=FunctionList, auth=[IsSuperuser(), IsStaff()])
def func_post(request, data: FunctionCreate):
    try:
        func = Function.objects.create(**data.dict())
        return {
                "id": func.id,
                "language": func.language,
                "problem": func.problem,
                "function": func.function,
                "user": func.user,
                "is_active": func.is_active,
                "created_at": func.created_at,
                "updated_at": func.updated_at
            }
    except Exception as e:
        raise HttpError(403, "nimadir xato ketti!")

@function_router_api.put("update/", response=FunctionList, auth=[IsSuperuser(), IsStaff()])
def func_update(request, id: int, data: FunctionCreate):
    try:
        func = Function.objects.get(id=id)
        for key, values in data.dict().item():
            setattr(func, key, values)
        func.save()
        return {
                "id": func.id,
                "language": func.language,
                "problem": func.problem,
                "function": func.function,
                "user": func.user,
                "is_active": func.is_active,
                "created_at": func.created_at,
                "updated_at": func.updated_at
            }
    except Exception as e:
        raise HttpError(404, "Topilmadi!")
    
@function_router_api.put("delete/", response=FunctionList, auth=[IsSuperuser(), IsStaff()])
def func_delete(request, id: int, data: FunctionCreate):
    try:
        func = Function.objects.get(id=id)
        func.delete()
        return {
                "id": func.id,
                "language": func.language,
                "problem": func.problem,
                "function": func.function,
                "user": func.user,
                "is_active": func.is_active,
                "created_at": func.created_at,
                "updated_at": func.updated_at
            }
    except Exception as e:
        raise HttpError(404, "Topilmadi!")