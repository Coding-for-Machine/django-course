from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
import random
import string
from courses.models import MyModules

def generate_slug_with_case(length=8):
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    slug = ''.join(random.choice(characters) for _ in range(length))
    return slug

class Language(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug_with_case(30)  # 10 uzunlikda tasodifiy slug yaratish
        super().save(*args, **kwargs)

    
# Dars modeli - har bir modulga tegishli darslarni saqlash uchun
class Lesson(models.Model):
    module = models.ForeignKey(MyModules, on_delete=models.CASCADE)  # Modulga bog'lanadi
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
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug_with_case(30)  # 10 uzunlikda tasodifiy slug yaratish
        super().save(*args, **kwargs)

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
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug_with_case(30)  # 10 uzunlikda tasodifiy slug yaratish
        super().save(*args, **kwargs)

class Function(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, related_name="functions", on_delete=models.CASCADE)
    function = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)  # Dars yaratish vaqti
    updated_at = models.DateTimeField(auto_now=True)  # Dars yangilanish vaqti
    def __str__(self):
        return self.function[:30]

class AlgorithmTest(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, related_name="test_cases", on_delete=models.CASCADE)
    algorithm = models.TextField()  # tugri kod kod
    created_at = models.DateTimeField(auto_now_add=True)  # Dars yaratish vaqti
    updated_at = models.DateTimeField(auto_now=True)  # Dars yangilanish vaqti
    def __str__(self):
        return self.algorithm[:30]
    
class TestCase(models.Model):
    algorithm = models.ForeignKey(AlgorithmTest, related_name="test_algorith", on_delete=models.CASCADE)
    input_data = models.CharField(max_length=200)
    output_data = models.CharField(max_length=200)

    def __str__(self):
        return f"Test for {self.algorithm.language.name}"



