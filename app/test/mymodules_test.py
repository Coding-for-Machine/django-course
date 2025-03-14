import pytest
from courses.models import MyModules, Course
from users.models import MyUser

@pytest.mark.django_db
def test_module_create():
    user = MyUser.objects.create(email="test@gmail.com", password="test")

    course = Course.objects.create(
        title="Test uchin 8888",
        slug="test-uchin",
        price=100,
        description="Beginner-friendly Python course",
        thumbnail="https://example.com/thumbnail.jpg",
        lesson_count=10,
        trailer="https://example.com/trailer.mp4",
        user=user
    )

    mymodule = MyModules.objects.create(
        course=course,
        title="My models",
        slug="my-model",
        description="My modules kiritildi va tekshirilmoqda",
        user=user
    )

    assert str(mymodule) == f"Module: {mymodule.title} (Course: {mymodule.course.title})"

    with pytest.raises(Exception):
        MyModules.objects.create(
            course=course,
            title="My models",
            slug="my-model",  
            description="My modules kiritildi va tekshirilmoqda",
            user=user
        )

    with pytest.raises(Exception):
        MyModules.objects.get(id=25) 
