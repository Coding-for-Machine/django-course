import pytest
from courses.models import Course
from users.models import MyUser

@pytest.mark.django_db
def test_create_course():
    # Foydalanuvchi yaratamiz (id ni belgilamaymiz)
    user = MyUser.objects.create(email="test@example.com", password="testpass")
    
    # Kurs yaratamiz
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
    
    # Kurs xususiyatlarini tekshiramiz
    assert course.title == "Asadbek"
    assert course.slug == "asadbek"
    assert course.price == 200
    assert course.description == "Asadbek"
    assert course.thumbnail == "https://github.com/Coding-for-Machine"
    assert course.lesson_count == 10
    assert course.trailer == "https://github.com/Coding-for-Machine"
    assert course.unlisted is True
    assert course.user == user

    # course update
    course_get = Course.objects.get(title="Asadbek")
    course_get.title = "Kamron"
    course_get.save()
    course_update = Course.objects.get(title="Kamron")
    assert course_update.title == "Kamron"

@pytest.mark.django_db
def test_course_title():
    user = MyUser.objects.create(
        email="testuchin@gmail.com",
        password="testuchin"
    )
    course = Course.objects.create(
        title = "Test uchin 8888",
        slug = "test-uchin",
        price=100,
        description="Beginner-friendly Python course",
        thumbnail="https://example.com/thumbnail.jpg",
        lesson_count=10,
        trailer="https://example.com/trailer.mp4",
        user=user
    )
    assert str(course)=="Test uchin 8888"


@pytest.mark.django_db
def test_course_slug_unique():
    user = MyUser.objects.create(
        email="testuchin@gmail.com",
        password="testuchin"
    )
    course = Course.objects.create(
        title = "Test uchin 8888",
        slug = "test-uchin",
        price=100,
        description="Beginner-friendly Python course",
        thumbnail="https://example.com/thumbnail.jpg",
        lesson_count=10,
        trailer="https://example.com/trailer.mp4",
        user=user
    )
    with pytest.raises(Exception):
        Course.objects.create(
            title = "Test uchin 8888",
            slug = "test-uchin",
            price=100,
            description="Beginner-friendly Python course",
            thumbnail="https://example.com/thumbnail.jpg",
            lesson_count=10,
            trailer="https://example.com/trailer.mp4",
            user=user
        )