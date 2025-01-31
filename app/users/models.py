from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, FileExtensionValidator

# Custom User Manager
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email field is required")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# Custom User Model
class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Email manzil")
    first_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="Ism")
    last_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="Familiya")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    is_staff = models.BooleanField(default=False, verbose_name="Xodim")
    is_deleted = models.BooleanField(default=False, verbose_name="O‘chirilgan")  # Soft delete
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti")

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def delete(self, *args, **kwargs):
        """Soft delete - foydalanuvchini bazadan o‘chirmasdan tizimdan olib tashlash"""
        self.is_deleted = True
        self.save()

    def restore(self):
        """Foydalanuvchini qayta tiklash"""
        self.is_deleted = False
        self.save()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['-created_at']


# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, verbose_name="Foydalanuvchi")
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ism")
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Familiya")
    image = models.ImageField(upload_to='profile/', default='user/user.png', blank=True, 
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], verbose_name="Profil rasmi")
    bio = models.TextField(blank=True, null=True, verbose_name="Bio")
    age = models.IntegerField(default=12, validators=[MinValueValidator(12)], verbose_name="Yosh")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.email})"

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profillar"
        ordering = ['-created_at']
