from ninja import Router
from ninja.errors import HttpError
from .auth_permission import IsStaff, IsSuperuser

# --------------- scheams ------------------
from pydantic import BaseModel
from typing import List
from datetime import datetime

class TestCaseList(BaseModel):
    id: int
    problem: int
    language: int
    input_data_top: str
    input_data_bottom: str
    user: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

class TestCaseCreate(BaseModel):
    problem: int
    language: int
    input_data_top: str
    input_data_bottom: str
    user: int
    is_active: bool

# --------------- crud admin ---------------

from lessons.models import TestCase

testcase_router_api = Router()
# get test case
@testcase_router_api.get("/", response=List[TestCaseList], auth=[IsSuperuser(), IsStaff()])
def test_case_get(request):
    return [
        {
            "id": testcase.id,
            "problem": testcase.problem,
            "language": testcase.language,
            "input_data_top": testcase.input_data_top,
            "input_data_bottom": testcase.input_data_bottom,
            "user": testcase.user,
            "is_active": testcase.is_active,
            "created_at": testcase.created_at,
            "updated_at": testcase.updated_at,
        }
        for testcase in TestCase.objects.all()
    ]
# test case get id
@testcase_router_api.get("{id}/", response=TestCaseList, auth=[IsSuperuser(), IsStaff()])
def test_case_get(request, id: int):
    try:
        testcase = TestCase.objects.all()
        return {
                "id": testcase.id,
                "problem": testcase.problem,
                "language": testcase.language,
                "input_data_top": testcase.input_data_top,
                "input_data_bottom": testcase.input_data_bottom,
                "user": testcase.user,
                "is_active": testcase.is_active,
                "created_at": testcase.created_at,
                "updated_at": testcase.updated_at,
            }
    except Exception as e:
        raise HttpError(404, "testcase topilmadi!")
    

# testcase create
@testcase_router_api.post("create/", response=TestCaseList, auth=[IsSuperuser(), IsStaff()])
def cerate_testcase_api(request, data: TestCaseCreate):
    try:
        testcase = TestCase.objects.create(**data.dict())
        return {
                "id": testcase.id,
                "problem": testcase.problem,
                "language": testcase.language,
                "input_data_top": testcase.input_data_top,
                "input_data_bottom": testcase.input_data_bottom,
                "user": testcase.user,
                "is_active": testcase.is_active,
                "created_at": testcase.created_at,
                "updated_at": testcase.updated_at,
            }
    except Exception as e:
        raise HttpError(403, "Nimadur Xato ketti!")
    
# testcase update
@testcase_router_api.put("update/", response=TestCaseList, auth=[IsSuperuser(), IsStaff()])
def update_testcase_api(request, id: int,data: TestCaseCreate):
    try:
        testcase = TestCase.objects.get(id=id)
        for key, value in data.dict().items():
            setattr(testcase, key, value)
        testcase.save()
        return {
                "id": testcase.id,
                "problem": testcase.problem,
                "language": testcase.language,
                "input_data_top": testcase.input_data_top,
                "input_data_bottom": testcase.input_data_bottom,
                "user": testcase.user,
                "is_active": testcase.is_active,
                "created_at": testcase.created_at,
                "updated_at": testcase.updated_at,
            }
    except TestCase.DoesNotExist:
        raise HttpError(404, "testcase topilmadi!")
    except Exception as e:
        raise HttpError(403, "Nimadur Xato ketti!")
    
# testcase delete
@testcase_router_api.delete("delete/", response=TestCaseList, auth=[IsSuperuser(), IsStaff()])
def delete_testcase_api(request, id: int,data: TestCaseCreate):
    try:
        testcase = TestCase.objects.get(id=id)
        testcase.delete()
        return {
                "id": testcase.id,
                "problem": testcase.problem,
                "language": testcase.language,
                "input_data_top": testcase.input_data_top,
                "input_data_bottom": testcase.input_data_bottom,
                "user": testcase.user,
                "is_active": testcase.is_active,
                "created_at": testcase.created_at,
                "updated_at": testcase.updated_at,
            }
    except Exception as e:
        raise HttpError(404, "Nimadur Xato ketti!")
    