from django.contrib.auth.models import User
from django.db import models
from users.models import MyUser
from courses.models import Module
from django_ckeditor_5.fields import CKEditor5Field


class Language(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name
    
# Dars modeli - har bir modulga tegishli darslarni saqlash uchun
class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)  # Modulga bog'lanadi
    title = models.CharField(max_length=255)  # Dars nomi
    slug = models.SlugField(unique=True)  # Dars uchun noyob identifikator
    lesson_type = models.CharField(
        max_length=50, 
        choices=[('darslik', 'darslik'), ('probelm', 'probelm')]  # Dars turi: lecture (teorik), lab (laboratoriya)
    )
    locked = models.BooleanField(default=False)  # Darsni qulflash holati (yopiq yoki ochiq)
    preview = models.BooleanField(default=False)  # Darsni preview qilish imkoniyati (tashrif buyurish)
    
    # Darslarni yaratish va yangilash vaqtlarini saqlash
    created_at = models.DateTimeField(auto_now_add=True)  # Dars yaratish vaqti
    updated_at = models.DateTimeField(auto_now=True)  # Dars yangilanish vaqti

    def __str__(self):
        return f"Lesson: {self.title} (Module: {self.module.title})"  # Dars nomi va tegishli modul nomini ko'rsatish

    class Meta:
        ordering = ['created_at']  # Darslar yaratish vaqtiga ko'ra tartiblanadi


class Problem(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    language = models.ManyToManyField(Language,related_name='problems_in_language')
    title = models.CharField(max_length=200, blank=True, null=True)
    description = CKEditor5Field(verbose_name='Darslik yoki Problems', config_name='extends')
    difficulty_choices = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    difficulty = models.CharField(choices=difficulty_choices, max_length=6)
    # Bu muammo uchun testlar va kod bo'limlari uchun qo'shimcha maydonlar bo'lishi mumkin.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class AlgorithmTest(models.Model):
    language = models.ForeignKey(Problem, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, related_name="test_cases", on_delete=models.CASCADE)
    algorithm = models.TextField()  # tugri kod kod
    algorithmtest = models.TextField()  # To'g'ri kod

    def __str__(self):
        return self.algorithm[:30]
    
class TestCase(models.Model):
    algorithm = models.ForeignKey(AlgorithmTest, related_name="test_cases", on_delete=models.CASCADE)
    input_data = models.CharField(max_length=200)
    output_data = models.CharField(max_length=200)

    def __str__(self):
        return f"Test for {self.problem.title}"



class Submission(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()  # Foydalanuvchi yuborgan kod
    status_choices = [
        ('pending', 'Pending'),
        ('correct', 'Correct'),
        ('incorrect', 'Incorrect'),
        ('error', 'Error'),
    ]
    status = models.CharField(choices=status_choices, default='pending', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Submission by {self.user.username} for {self.problem.title}"
