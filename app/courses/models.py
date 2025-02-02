from django.db import models
from users.models import MyUser
from django.utils.text import slugify


class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    price = models.PositiveIntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    lesson_count = models.PositiveIntegerField(blank=True, null=True)
    trailer = models.URLField(blank=True, null=True)
    unlisted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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


class Enrollment(models.Model):
    user = models.ForeignKey(MyUser, related_name='enrollments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} enrolled in {self.course.title}"


class Payment(models.Model):
    enrollment = models.OneToOneField(Enrollment, related_name='payment', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    payment_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')])
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.enrollment.course.title} by {self.enrollment.user.username}"


class MyModules(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)  # "related_name" qo‘shildi
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
