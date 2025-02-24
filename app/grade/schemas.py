from pydantic import BaseModel
from datetime import datetime

#  Grade baholash jadvali Schemasi cerated
class GradeSchemasCreate(BaseModel):
    student: str
    teacher: str
    problems: str
    score: int
    comment: str = None

#  Grade baholash jadvali Schemasi list
class GradeSchemasList(GradeSchemasCreate):
    created: datetime


#  Group schemas cerated
class GroupSchemasCreated(BaseModel):
    name: str
    owner: str
    students: str
    


