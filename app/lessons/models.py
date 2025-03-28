from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from .generate_slug import generate_slug_with_case
from courses.models import MyModules
from courses.models import TimeMixsin
from users.models import MyUser


class Language(TimeMixsin):
    name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug_with_case(30)  # 10 uzunlikda tasodifiy slug yaratish

        super().save(*args, **kwargs)
    
    
class Lesson(TimeMixsin):
    module = models.ForeignKey(MyModules, related_name="lesson", on_delete=models.CASCADE)  # Modulga bog'lanadi
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)
    lesson_type = models.CharField(
        max_length=50, 
        choices=[('darslik', 'darslik'), ('probelm', 'probelm')]  
    )
    preview = models.BooleanField(default=False)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Lesson: (Module: {self.module.title})"  
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug_with_case(30)
        super().save(*args, **kwargs)

    # class Meta:
    #     ordering = ['created_at'] 
    #     indexes = [
    #         models.Index(["user", "created"])
    #     ]


class Problem(TimeMixsin):
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
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        if self.title:
            return self.title
        return self.difficulty
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug_with_case(30)  # 10 uzunlikda tasodifiy slug yaratish
        super().save(*args, **kwargs)


class Function(TimeMixsin):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, related_name="functions", on_delete=models.CASCADE)
    function = models.TextField()
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    def __str__(self):
        return self.function[:30]


class TestCase(TimeMixsin):
    problem = models.ForeignKey("Problem", related_name="test_algorith", on_delete=models.CASCADE)
    language = models.ForeignKey(Language, related_name="test_language", on_delete=models.CASCADE)
    input_data_top = models.TextField(help_text="Test yuqori qismi")
    input_data_bottom = models.TextField(help_text="Pastki qismi")
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    def __str__(self):
        return f"Test for {self.problem.title}"




