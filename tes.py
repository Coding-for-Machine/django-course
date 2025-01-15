from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    price = models.PositiveIntegerField()
    enrolled = models.BooleanField(default=False)
    description = models.TextField()
    trailer = models.URLField()
    thumbnail = models.URLField()
    lesson_count = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    # Kursga o'qigan foydalanuvchilarning progressini hisoblash
    def get_progress(self, user):
        total_lessons = self.lesson_count
        completed_lessons = user.progress.filter(lesson__module__course=self, is_completed=True).count()
        return (completed_lessons / total_lessons) * 100 if total_lessons else 0

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    lesson_type = models.CharField(max_length=50)  # "lecture" or "lab"
    locked = models.BooleanField(default=False)
    preview = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# Foydalanuvchi kurs va dars bo'yicha progressini saqlash uchun model
class Progress(models.Model):
    user = models.ForeignKey(User, related_name='progress', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='progress', on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} - {'Completed' if self.is_completed else 'Incomplete'}"

# Kursni baholash va sharhlar qo'shish uchun model
class Rating(models.Model):
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='ratings', on_delete=models.CASCADE)
    score = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 baholar
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.score}"

# Kurs yoki darsga sharh qo'shish uchun model
class Review(models.Model):
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='reviews', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
