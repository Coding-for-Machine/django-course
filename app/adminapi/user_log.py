from ninja import Router
from pydantic import BaseModel
from easyaudit.models import CRUDEvent
from datetime import datetime as dt
from typing import List
# router
user_log = Router()

class CRUDEventSchemas(BaseModel):
    id: int
    event_type: int
    object_id: int
    object_repr: str
    datetime: dt


@user_log.get("log/", response=List[CRUDEventSchemas])
def user_log(request):
    pass
