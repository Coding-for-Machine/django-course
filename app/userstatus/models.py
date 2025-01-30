from django.db import models
from lessons.models import Lesson
from users.models import MyUser
# Create your models here.

class UserLessonStatus(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    