from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class SomeModel(models.Model):
    def get_module(self):
        from courses.models import Module

class Language(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name
    
# class AdvancedTest(models.Model):
#     code = models.TextField()
#     def __str__(self):
#         return f"{self.id}---AdvancedTest"
    
# Dars modeli - har bir modulga tegishli darslarni saqlash uchun
class Lesson(models.Model):
    module = models.ForeignKey(SomeModel, on_delete=models.CASCADE)  # Modulga bog'lanadi
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
        return f"Lesson: (Module: {self.module.title})"  # Dars nomi va tegishli modul nomini ko'rsatish

    class Meta:
        ordering = ['created_at']  # Darslar yaratish vaqtiga ko'ra tartiblanadi


class Problem(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    language = models.ManyToManyField(Language,related_name='problems_in_language')
    title = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=250, blank=True, null=True)
    description = CKEditor5Field(verbose_name='Darslik yoki Problems', config_name='extends')
    difficulty_choices = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    difficulty = models.CharField(choices=difficulty_choices, max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.title:
            return self.title
        return self.difficulty
    

class AlgorithmTest(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, related_name="test_cases", on_delete=models.CASCADE)
    algorithm = models.TextField()  # tugri kod kod

    def __str__(self):
        return self.algorithm[:30]
    
class TestCase(models.Model):
    algorithm = models.ForeignKey(AlgorithmTest, related_name="test_algorith", on_delete=models.CASCADE)
    input_data = models.CharField(max_length=200)
    output_data = models.CharField(max_length=200)

    def __str__(self):
        return f"Test for {self.algorithm.language.name}"



