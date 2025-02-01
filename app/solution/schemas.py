from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

# ✅ Base Model (Barcha schema'lar uchun umumiy sozlamalar)
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # ORM Mode


# ✅ Solution Schema
class SolutionSchema(BaseSchema):
    user_id: int = Field(..., description="Foydalanuvchi ID si")
    problem_id: int = Field(..., description="Muammo (problem) ID si")
    language_id: int = Field(..., description="Dasturlash tili ID si")
    code: str = Field(..., description="Foydalanuvchining kod yechimi")
    execution_time: float = Field(0.0, description="Bajarilish vaqti (sekund)")
    memory_usage: float = Field(0.0, description="Xotira ishlatilishi (MB)")
    passed_tests: int = Field(0, description="O'tgan testlar soni")
    total_tests: int = Field(0, description="Jami testlar soni")

class SolutionOutSchema(SolutionSchema):
    score: int = Field(0, description="Foydalanuvchi bahosi")
    is_accepted: bool = Field(False, description="Qabul qilindi yoki yo'q")


# ✅ User Quiz Result Schema
class UserQuizResultSchema(BaseSchema):
    user_id: int = Field(..., description="Foydalanuvchi ID si")
    quiz_id: int = Field(..., description="Quiz ID si")
    correct_answers: int = Field(..., description="To'g'ri javoblar soni")
    total_questions: int = Field(..., description="Jami savollar soni")

class UserQuizResultOutSchema(UserQuizResultSchema):
    score: int = Field(..., description="Foydalanuvchi to'plagan ballari")


# ✅ User Question Result Schema
class UserQuestionResultSchema(BaseSchema):
    user_id: int = Field(..., description="Foydalanuvchi ID si")
    question_id: int = Field(..., description="Savol ID si")
    is_correct: bool = Field(..., description="Javob to‘g‘rimi yoki noto‘g‘ri")
