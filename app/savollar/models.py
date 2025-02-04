import uuid
from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django_ckeditor_5.fields import CKEditor5Field
from users.models import MyUser
from django.utils.text import slugify
from courses.models import MyModules


# Unikal slug yaratish funksiyasi
def generate_unique_slug(model_class, title):
    slug = slugify(title)
    while model_class.objects.filter(slug=slug).exists():
        slug = f"{slug}-{uuid.uuid4().hex[:6]}"
    return slug


# ==========================
# 2. Quiz modeli
# ==========================
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = CKEditor5Field(verbose_name='Savol', config_name='extends')
    MyModules = models.ForeignKey(MyModules, related_name='quizzes', on_delete=models.CASCADE)
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


def generate_unique_slug(model_class, title):
    """Berilgan sarlavha bo‘yicha unikal slug yaratish"""
    base_slug = slugify(title)
    slug = base_slug
    counter = 1
    while model_class.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = CKEditor5Field(verbose_name='Savol', config_name='extends')
    MyModules = models.ForeignKey(MyModules, related_name='quizzes', on_delete=models.CASCADE)
    time_limit = models.PositiveIntegerField(default=600)  # Sekundlarda (10 daqiqa)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def save(self, *args, **kwargs):
        """Agar slug bo'lmasa, avtomatik unikal slug yaratish"""
        if not self.slug:
            self.slug = generate_unique_slug(Quiz, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_time_limit_display(self):
        """Vaqtni daqiqa va sekund shaklida qaytarish"""
        minutes = self.time_limit // 60
        seconds = self.time_limit % 60
        return f"{minutes} min {seconds} sec"

    def get_total_questions(self):
        """Quizda nechta savol borligini hisoblash"""
        return self.questions.count()  # Agar `Question` modeli mavjud bo‘lsa

    def calculate_score_percentage(self, correct_answers, total_questions):
        """Foiz hisoblash"""
        if total_questions == 0:
            return 0
        return round((correct_answers / total_questions) * 100, 2)



# ==========================
# 4. Question modeli (Quiz va Topic uchun umumiy)
# ==========================
class Question(models.Model):
    content_type = models.ForeignKey(ContentType, related_name="questions",on_delete=models.CASCADE)  # Model turi (Quiz yoki Topic)
    object_id = models.PositiveIntegerField()  # Bog‘langan model ID si
    content_object = GenericForeignKey('content_type', 'object_id')  # GenericForeignKey
    description = CKEditor5Field(verbose_name='Savol', config_name='extends')
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
        return f"{self.get_related_object()} - {self.description[:50]}"

    def get_related_object(self):
        """Bog‘langan model obyektini qaytaradi (Quiz yoki Topic)"""
        return self.content_object

    def get_quiz_or_topic_name(self):
        """Quiz yoki Topic nomini qaytarish"""
        related_object = self.get_related_object()
        return related_object.description if hasattr(related_object, 'title') else related_object.description

    def get_model_type(self):
        """Savol qaysi modelga tegishli ekanligini qaytaradi"""
        return self.content_type.model


# ==========================
# 5. Answer modeli (Javob variantlari)
# ==========================
class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    description = CKEditor5Field(verbose_name='Savol', config_name='extends')
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return f"{self.description}"

