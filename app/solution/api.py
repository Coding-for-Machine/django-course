from ninja import Router
from django.shortcuts import get_object_or_404
from .models import Solution, UserQuizResult, UserQuestionResult
from users.models import MyUser
from lessons.models import Problem, Language, TestCase
from savollar.models import Quiz, Question
from ninja import Router, Schema
# from .run_code_api import format_code_push
from .schemas import *

solution_url_api = Router()


from typing import List


# 📝 Schema - Kiruvchi va chiquvchi ma'lumotlarni aniqlash
class SolutionSchema(Schema):
    user_id: int
    problem_id: int
    language_id: int
    code: str

class SolutionResponseSchema(Schema):
    id: int
    user_id: int
    problem_id: int
    language_id: int
    code: str
    is_accepted: bool
    execution_time: float
    memory_usage: float
    score: int
    passed_tests: int
    total_tests: int
    created_at: str
    updated_at: str

# 🚀 Foydalanuvchi yechimini yaratish (POST)
@solution_url_api.post("/solutions/", response=SolutionResponseSchema)
def create_solution(request, payload: SolutionSchema):
    # if not request.user.is_authenticatid:
    #     return None
    # user = request.user
    # # user = get_object_or_404(MyUser, id=payload.user_id)
    # problem = get_object_or_404(Problem, id=payload.problem_id)
    # language = get_object_or_404(Language, id=payload.language_id)
    # # get test case
    # test_case = get_object_or_404(TestCase, problem=problem, language=language)
    # if payload.code and language:
    #     response = format_code_push(language, payload.code, test_case)

    #     solution = Solution.objects.create(
    #         user=user,
    #         problem=problem,
    #         language=language,
    #         code=response.code,
    #         is_accepted=response.is_accepted,
    #         execution_time=response.execution_time,
    #         memory_usage=response.memory_usage
    #     )
        
    # return solution
    pass

# 📌 Barcha yechimlarni olish (GET)
@solution_url_api.get("/solutions/", response=List[SolutionResponseSchema])
def get_solutions(request):
    return Solution.objects.all()

# 🎯 Muayyan foydalanuvchining yechimlarini olish
@solution_url_api.get("/solutions/user/{user_id}", response=List[SolutionResponseSchema])
def get_user_solutions(request, user_id: int):
    return Solution.objects.filter(user__id=user_id)

# 🎯 Muayyan masalaga oid yechimlarni olish
@solution_url_api.get("/solutions/problem/{problem_id}", response=List[SolutionResponseSchema])
def get_problem_solutions(request, problem_id: int):
    return Solution.objects.filter(problem__id=problem_id)



# ✅ UserQuizResult yaratish (POST)
@solution_url_api.post("/quiz-results", response=UserQuizResultSchema)
def create_quiz_result(request, data: UserQuizResultSchema):
    user = get_object_or_404(MyUser, id=data.user_id)
    quiz = get_object_or_404(Quiz, id=data.quiz_id)

    result = UserQuizResult.log_quiz_result(
        user=user,
        quiz=quiz,
        correct_answers=data.correct_answers,
        total_questions=data.total_questions
    )
    return result


# ✅ UserQuestionResult yaratish (POST)
@solution_url_api.post("/question-results", response=UserQuestionResultSchema)
def create_question_result(request, data: UserQuestionResultSchema):
    user = get_object_or_404(MyUser, id=data.user_id)
    question = get_object_or_404(Question, id=data.question_id)

    result = UserQuestionResult.log_answer(
        user=user,
        question=question,
        is_correct=data.is_correct
    )
    return result


