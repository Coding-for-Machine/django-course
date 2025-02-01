from ninja import Router
from django.shortcuts import get_object_or_404
from .models import Solution, UserQuizResult, UserQuestionResult
from users.models import MyUser
from lessons.models import Problem, Language
from savollar.models import Quiz, Question

from .schemas import *

solution_url_api = Router()


# ✅ Solution yaratish (POST)
@solution_url_api.post("/solutions", response=SolutionSchema)
def create_solution(request, data: SolutionSchema):
    user = get_object_or_404(MyUser, id=data.user_id)
    problem = get_object_or_404(Problem, id=data.problem_id)
    language = get_object_or_404(Language, id=data.language_id)

    solution = Solution.log_solution(
        user=user,
        problem=problem,
        language=language,
        code=data.code,
        execution_time=data.execution_time,
        memory_usage=data.memory_usage,
        passed_tests=data.passed_tests,
        total_tests=data.total_tests
    )
    return solution


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


