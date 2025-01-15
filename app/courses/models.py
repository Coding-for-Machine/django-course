from django.db import models
# Kurs modeli - kurslar haqida asosiy ma'lumotlarni saqlash uchun
from django.contrib.auth.models import User

class Course(models.Model):
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
        Kursni saqlashdan oldin, ushbu kursga tegishli darslar sonini hisoblab,
        'lesson_count' maydonini yangilash.
        """
        # Kursda biror modul mavjud bo'lsa, darslar sonini hisoblash
        if self.pk:  # Agar primary key mavjud bo'lsa
            self.lesson_count = self.modules.aggregate(models.Count('lessons'))['lessons__count']
        super().save(*args, **kwargs)  # Asl saqlashni amalga oshirish


class Enrollment(models.Model):
    user = models.ForeignKey(User, related_name='enrollments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)  # To'lov tasdiqlanganligi
    # Har bir kurs yaratganingizda yoki yangilaganingizda ishlatiladigan vaqt maydonlari
    created_at = models.DateTimeField(auto_now_add=True)  # Kurs yaratish vaqti
    updated_at = models.DateTimeField(auto_now=True)  # Kursni so'nggi marta yangilash vaqti

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"


class Payment(models.Model):
    enrollment = models.OneToOneField(Enrollment, related_name='payment', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    payment_status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')])
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.enrollment.course.title} by {self.enrollment.user.username}"



# Modul modeli - har bir kursga tegishli bo'lgan modullarni saqlash uchun
class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)  # Kursga bog'lanadi
    title = models.CharField(max_length=255)  # Modul nomi
    slug = models.SlugField(unique=True)  # Modul uchun noyob identifikator
    description = models.TextField(blank=True, null=True)  # Modul tavsifi (ixtiyoriy)
    # Har bir modul yaratish va yangilash vaqtlarini saqlash
    created_at = models.DateTimeField(auto_now_add=True)  # Modul yaratish vaqti
    updated_at = models.DateTimeField(auto_now=True)  # Modul yangilanish vaqti

    def __str__(self):
        return f"Module: {self.title} (Course: {self.course.title})"  # Modul nomi va tegishli kurs nomini ko'rsatish
