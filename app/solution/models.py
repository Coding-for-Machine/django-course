from django.db import models
from django.contrib.auth.models import User
from lessons.models import Problem


# Foydalanuvchining yechimi
class Solution(models.Model):
    user = models.ForeignKey(User, related_name='solutions', on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, related_name='solutions', on_delete=models.CASCADE)
    code = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)  # Dars yaratish vaqti
    updated_at = models.DateTimeField(auto_now=True)  # Dars yangilanish vaqti
    def __str__(self):
        return f"{self.user.username} - {self.problem.title} - {'Accepted' if self.is_accepted else 'Pending'}"