from django.db import models
from users.models import MyUser
from lessons.models import Problem
# from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
import random
# Create your models here.



class SavolQuerySet(models.QuerySet):
    def Asanroq(self):
        return self.filter(savol_turi="ASN")

    def Ortacha(self):
        return self.filter(savol_turi="ORT")

    
    def Qiyin(self):
        return self.filter(savol_turi="QYN")
    
    
class SavolManager(models.Manager):
    def get_queryset(self):
        return SavolQuerySet(self.model, using=self._db)

    def Asanroq(self):
        return self.get_queryset().Asanroq()

    def Ortacha(self):
        return self.get_queryset().Ortacha()
    
    def Qiyin(self):
        return self.get_queryset().Qiyin()

class Savol(models.Model):
    SAVOL_TURI=[
       ("ASN" , "Asonroq Savol"),
       ("ORT" , "O\'rtacha Savol"),
       ("QYN" , "Qiyin Savol"),
    ]
    description = CKEditor5Field(verbose_name='Savol', config_name='extends')
    problems = models.ForeignKey(Problem, on_delete=models.CASCADE)
    quizes_types = models.CharField(max_length=3, choices=SAVOL_TURI, default="ORT")

    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    objects=SavolManager()
    def __str__(self) -> str:
        return str(self.description)
    
    def get_answers(self):
        savol=list(self.varyant_set.all())
        random.shuffle(savol)
        return savol

class Varyant(models.Model):
    savol=models.ForeignKey(Savol, on_delete=models.CASCADE)
    description = CKEditor5Field(verbose_name='Savol', config_name='extends')
    tugri_yoke_natugri=models.BooleanField(default=False, help_text="To\'g\'ri varionad bo\'lsa ptichka qo\'ying!!")
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return f"{self.savol.description} | Javob: {self.description} | To'g'ri: {self.tugri_yoke_natugri}"

class Results(models.Model):
    quiz = models.ForeignKey(Savol, on_delete=models.CASCADE, related_name="results")
    user=models.ForeignKey(MyUser, on_delete=models.CASCADE)
    javob = models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)
    
    class Meta:
        verbose_name = "Javoblar"
        verbose_name_plural = "Javoblar"
    

import uuid
from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from users.models import MyUser


# Unikal slug yaratish funksiyasi
def generate_unique_slug(model_class, title):
    slug = slugify(title)
    while model_class.objects.filter(slug=slug).exists():
        slug = f"{slug}-{uuid.uuid4().hex[:6]}"
    return slug


# ==========================
# 1. Kategoriya modeli
# ==========================
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Category, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ==========================
# 2. Quiz modeli
# ==========================
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, related_name='quizzes', on_delete=models.CASCADE)
    time_limit = models.PositiveIntegerField(default=10)  # daqiqalarda
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Quiz, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ==========================
# 3. Topic modeli
# ==========================
class Topic(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, related_name='topics', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Topic"
        verbose_name_plural = "Topics"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Topic, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ==========================
# 4. Question modeli (Quiz va Topic uchun umumiy)
# ==========================
class Question(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Model turi (Quiz yoki Topic)
    object_id = models.PositiveIntegerField()  # Bog‘langan model ID si
    content_object = GenericForeignKey('content_type', 'object_id')  # GenericForeignKey
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def save(self, *args, **kwargs):
        # content_object bo'lsa, content_type va object_id ni to'ldirish
        if self.content_object:
            self.content_type = ContentType.objects.get_for_model(self.content_object.__class__)
            self.object_id = self.content_object.id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_related_object()} - {self.text[:50]}"

    def get_related_object(self):
        """Bog‘langan model obyektini qaytaradi (Quiz yoki Topic)"""
        return self.content_object

    def get_quiz_or_topic_name(self):
        """Quiz yoki Topic nomini qaytarish"""
        related_object = self.get_related_object()
        return related_object.title if hasattr(related_object, 'title') else related_object.name

    def get_model_type(self):
        """Savol qaysi modelga tegishli ekanligini qaytaradi"""
        return self.content_type.model


# ==========================
# 5. Answer modeli (Javob variantlari)
# ==========================
class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Wrong'})"


# ==========================
# 6. UserScore modeli (Test natijalari)
# ==========================
class UserScore(models.Model):
    user = models.ForeignKey(MyUser, related_name='scores', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='scores', on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']
        verbose_name = "User Score"
        verbose_name_plural = "User Scores"

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}: {self.score}"

    def calculate_score(self):
        """Foydalanuvchi ballini hisoblash"""
        correct_answers = UserAnswer.objects.filter(
            user=self.user,
            question__content_type=ContentType.objects.get_for_model(Quiz),
            question__object_id=self.quiz.id,
            answer__is_correct=True
        ).count()
        total_questions = self.quiz.questions.count()
        self.score = int((correct_answers / total_questions) * 100) if total_questions > 0 else 0
        self.save()


# ==========================
# 7. UserAnswer modeli (Foydalanuvchining javoblari)
# ==========================
class UserAnswer(models.Model):
    user = models.ForeignKey(MyUser, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='user_answers', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, related_name='user_answers', on_delete=models.CASCADE)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Answer"
        verbose_name_plural = "User Answers"

    def __str__(self):
        return f"{self.user.username} - {self.question.text[:30]}: {self.answer.text}"
