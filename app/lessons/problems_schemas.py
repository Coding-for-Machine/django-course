from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Test Case Schema
class TestCaseSchema(BaseModel):
    input_data: str
    output_data: str

    class Config:
        orm_mode = True  # Django ORM obyektlarini to'g'ri seriyalash

class LanguageSchema(BaseModel):
    name: str
    slug: str
    class Config:
        orm_mode =True

# advanced_test
class AdvancedTestSchema(BaseModel):
    code: str
    class Config:
        orm_mode = True  

# AlgorithmTest Schema
class AlgorithmTestSchema(BaseModel):
    algorithm: str
    algorithmtest: str
    language: List[LanguageSchema]
    advanced_test: List[AdvancedTestSchema]
    test_cases: List[TestCaseSchema]

    class Config:
        orm_mode = True

# Problem Schema
class ProblemSchema(BaseModel):
    id: int
    title: str
    slug: str | None
    description: str
    difficulty: str
    test_cases: List[AlgorithmTestSchema]  # Muammoga tegishli testlar
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

