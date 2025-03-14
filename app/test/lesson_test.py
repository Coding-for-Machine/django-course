import pytest
from lessons.models import Lesson, Problem, Language
from courses.models import Course, MyModules
from users.models import MyUser


@pytest.mark.django_db
def test_lesson_create():
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
    module_get = MyModules.objects.get(
        title="My models"
    )
    assert lesson.title in [l.title for l in module_get.lesson.all()]
    with pytest.raises(Exception):
        lesson = Lesson.objects.get(
            id=404
    )
        
@pytest.mark.django_db
def test_problem():
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
    module_get = MyModules.objects.get(
        title="My models"
    )
    assert lesson.title in [l.title for l in module_get.lesson.all()]
    with pytest.raises(Exception):
        lesson = Lesson.objects.get(
            id=404
    )
    # language
    language = Language.objects.create(
        name="python"
    )
    # problemni test qilamiz
    problem = Problem.objects.create(
        lesson=lesson,
        title="pythonda linked list",
        description="python juda yaxshi til",
        difficulty="medium",
        user=user
    )
    # problem.language.add(language1, language2, language3)
    problem.language.set([language])
    problem_get = Problem.objects.get(title="pythonda linked list")
    assert problem_get.title == "pythonda linked list"

        

      