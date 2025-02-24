from django.db import models
from users.models import MyUser
from lessons.models import Problem
# Create your models here.
from courses.models import TimeMixsin

class Comments(TimeMixsin):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    problems = models.ForeignKey(Problem, on_delete=models.CASCADE)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email}--{self.problems.lesson.title}--{self.comments[:30]}"
