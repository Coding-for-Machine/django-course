from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ninja import Router

from .problems_schemas import ProblemSchema
from .models import AlgorithmTest, Lesson, Problem, TestCase
from savollar.models import Question, Answer

problems_api = Router()

@problems_api.get("/{slug_lesson}/{slug}", response=ProblemSchema)
def problems_dateal(request, slug_lesson, slug):
    lesson = get_object_or_404(Lesson, slug=slug_lesson)
    if lesson:
        problems = Problem.objects.filter(slug=slug)

        # Lesson ma'lumotlarini yaratish
        lesson_data = {
            "problems": [
                {
                    "id": problem.id,
                    "title": problem.title,
                    "slug": problem.slug,
                    "description": problem.description,
                    "difficulty": problem.difficulty,
                    "created_at": problem.created_at,
                    "updated_at": problem.updated_at,
                    "algoritm": [
                        {
                            "language": algorithm_test.language.name,
                            "algorithm": algorithm_test.algorithm,
                            "algorithmtest": algorithm_test.algorithmtest,
                            "advanced_test": algorithm_test.advanced_test.code,
                            "test_cases": [
                                {
                                    "input_data": test_case.input_data,
                                    "output_data": test_case.output_data
                                }
                                for test_case in TestCase.objects.filter(algorithm=algorithm_test)[:3]
                            ]
                        }
                        for algorithm_test in AlgorithmTest.objects.filter(problem=problem)
                    ],
                    "test": [
                        {
                            "id": savol.id,
                            "description": savol.description,
                            "quizes_types": savol.quizes_types,
                            "created": savol.created,
                            "updated": savol.updated,
                            "varyantlar": [
                                {
                                    "id": varyant.id,
                                    "description": varyant.description,
                                    "tugri_yoke_natugri": varyant.tugri_yoke_natugri,
                                    "created": varyant.created,
                                    "updated": varyant.updated,
                                }
                                for varyant in Answer.objects.filter(savol=savol)
                            ],
                        }
                        for savol in Question.objects.filter(problems=problem)
                    ],
                }
                for problem in problems
            ]
        }
        return JsonResponse(lesson_data)
    return JsonResponse({"error": "Darslik topilmadi"})
