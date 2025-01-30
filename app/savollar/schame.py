from  pydantic import BaseModel
from datetime import datetime
from typing import Literal, Any

class SavolSchema(BaseModel):
    id: int
    description: str
    problems: str
    quizes_types: Literal["ASN", "ORT", "QYN"]
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class VaryantSchema(BaseModel):
    id: int
    savol: SavolSchema
    description: Any
    tugri_yoke_natugri: bool
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class ResultsSchema(BaseModel):
    quiz: SavolSchema
    user: str
    javob: bool
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True
