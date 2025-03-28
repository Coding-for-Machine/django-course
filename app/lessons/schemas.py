from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Test Case Schema
class TestCaseSchema(BaseModel):
    input_data: str
    output_data: str

    class Config:
        orm_mode = True  # Django ORM obyektlarini to'g'ri seriyalash

# AlgorithmTest Schema
class AlgorithmTestSchema(BaseModel):
    algorithm: str
    algorithmtest: str
    test_cases: List[TestCaseSchema]

    class Config:
        orm_mode = True

# Problem Schema
class ProblemSchema(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str
    test_cases: List[AlgorithmTestSchema]  # Muammoga tegishli testlar
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Lesson Schema
class LessonSchema(BaseModel):
    id: int
    title: str
    slug: str
    lesson_type: str
    locked: bool
    preview: bool
    created_at: datetime
    updated_at: datetime
    problems: List[ProblemSchema]  # Darsga tegishli muammolar

    class Config:
        orm_mode = True
