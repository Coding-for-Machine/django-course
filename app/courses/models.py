from django.db import models
from users.models import MyUser
from django.utils.text import slugify


#  base timemixis
class TimeMixsin(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract=True
        # model yaratmaydi abstract=True

class Course(TimeMixsin):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    price = models.PositiveIntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    lesson_count = models.PositiveIntegerField(blank=True, null=True)
    trailer = models.URLField(blank=True, null=True)
    unlisted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Kursni saqlashdan oldin darslar sonini hisoblash.
        """
        # Avval kursni saqlaymiz, chunki yangi yaratilgan kursda PK (ID) yo'q
        is_new = self.pk is None  # Yangi kurs ekanligini tekshiramiz
        super().save(*args, **kwargs)  # Avval kursni bazaga saqlaymiz
        
        # Agar kurs avvaldan mavjud bo‘lsa, unga bog‘langan modullarni hisoblash
        if not is_new:
            self.lesson_count = sum(module.lesson.all().count() for module in self.modules.all())  # "module_set" emas, "modules"
            super().save(update_fields=['lesson_count'])  # Faqat lesson_count yangilanadi


class Enrollment(TimeMixsin):
    user = models.ForeignKey(MyUser, related_name='enrollments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} enrolled in {self.course.title}"


class MyModules(TimeMixsin):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)  # "related_name" qo‘shildi
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Module: {self.title} (Course: {self.course.title})"

    def __str__(self):
        return f"Module: {self.title} (Course: {self.course.title})"

    def save(self, *args, **kwargs):
        """
        Modul saqlanishidan oldin slugni yaratish.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
