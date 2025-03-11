from django.db import models
# from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django_ckeditor_5.fields import CKEditor5Field
from users.models import MyUser
from courses.models import MyModules
from .generate_slug import generate_unique_slug
from courses.models import TimeMixsin




class Quiz(TimeMixsin):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = CKEditor5Field(verbose_name='Savol', config_name='extends')
    MyModules = models.ForeignKey(MyModules, related_name='quizzes', on_delete=models.CASCADE)
    time_limit = models.PositiveIntegerField(default=600)  # Sekundlarda (10 daqiqa)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
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

    def get_time_limit_display(self):
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



class Question(TimeMixsin):
    content_type = models.ForeignKey(ContentType, related_name="questions",on_delete=models.CASCADE)  # Model turi (Quiz yoki Topic)
    object_id = models.PositiveIntegerField()  # Bog‘langan model ID si
    content_object = GenericForeignKey('content_type', 'object_id')  # GenericForeignKey
    description = CKEditor5Field(verbose_name='Savol', config_name='extends')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    class Meta:
        ordering = ['-created_at']
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
        return self.content_object

    def get_quiz_or_topic_name(self):
        related_object = self.get_related_object()
        return related_object.description if hasattr(related_object, 'title') else related_object.description

    def get_model_type(self):
        return self.content_type.model



class Answer(TimeMixsin):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    description = CKEditor5Field(verbose_name='Savol', config_name='extends')
    is_correct = models.BooleanField(default=False)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "User-Javob"
        verbose_name_plural = "User-Javoblari"

    def __str__(self):
        return f"{self.description}"


