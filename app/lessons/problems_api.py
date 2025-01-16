from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ninja import Router

from .problems_schemas import ProblemSchema
from .models import AlgorithmTest, Lesson, Problem, TestCase

problems_api = Router()

@problems_api.get("/{slug_lesson}/{slug}", response=ProblemSchema)
def problems_dateal(request, slug_lesson, slug):
    lesson = get_object_or_404(Lesson, slug=slug_lesson)
    if lesson:
        problems = Problem.objects.filter(slug=slug)
    
    # Lesson ma'lumotlarini yaratish
        lesson_data ={
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
                    ]
                }
                for problem in problems
            ]}
        return JsonResponse(lesson_data)
    return JsonResponse({"error": "darslik topilmadi"})

