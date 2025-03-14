import pytest
from lessons.models import Lesson, Problem, Language, TestCase
from courses.models import Course, MyModules
from users.models import MyUser


@pytest.fixture
def setup():
    user = MyUser.objects.create(
        email="123456@gmail.com",
        password="1234567"
    )
    course = Course.objects.create(
        title="Asadbek",
        slug="asadbek",
        price=200,
        description="Asadbek",
        thumbnail="https://github.com/Coding-for-Machine",
        lesson_count=10,
        trailer="https://github.com/Coding-for-Machine",
        unlisted=True,
        user=user
    )
    module = MyModules.objects.create(
        course=course,
        title="My models",
        slug="my-model",
        description="My modules kiritildi va tekshirilmoqda",
        user=user
    )
    lesson = Lesson.objects.create(
        module=module,
        title="my lesson test uchin",
        user=user
    )
    problem = Problem.objects.create(
        lesson=lesson,
        title="pythonda linked list",
        description="python juda yaxshi til",
        difficulty="medium",
        user=user
    )
    language = Language.objects.create(
        name="python"
    )
    return user, course, module, lesson, problem, language


@pytest.mark.django_db
def test_lesson_create(setup):
    user, course, module, lesson, problem, language = setup  # ✅ TO‘G‘RI
    module_get = MyModules.objects.get(title="My models")
    assert lesson.title in [l.title for l in module_get.lesson.all()]
    with pytest.raises(Exception):
        Lesson.objects.get(id=404)


@pytest.mark.django_db
def test_problem(setup):
    user, course, module, lesson, problem, language = setup  # ✅ TO‘G‘RI
    problem.language.set([language])
    
    problem_get = Problem.objects.get(title="pythonda linked list")
    assert problem_get.title == "pythonda linked list"

@pytest.mark.django_db
def test_testcase(setup):
    user, course, module, lesson, problem, language = setup  # ✅ TO‘G‘RI
    testcase = TestCase.objects.create(
        problem=problem,
        language=language,
        input_data_top="import pytest",
        input_data_bottom="# run test",
        user=user
    )
    assert str(testcase) == f"Test for {problem.title}"  # ✅ TO‘G‘RI
