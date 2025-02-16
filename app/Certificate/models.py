import qrcode
from io import BytesIO
from django.db import models
from users.models import MyUser
from courses.models import Course
from django.core.files.base import ContentFile


class SiteSettings(models.Model):
    """Admin tomonidan boshqariladigan sayt sozlamalari"""
    certificate_base_url = models.URLField(default="https://yourwebsite.com/certificate/")

    def __str__(self):
        return "Sayt sozlamalari"

    class Meta:
        verbose_name = "Sayt Sozlamasi"
        verbose_name_plural = "Sayt Sozlamalari"


class Organization(models.Model):
    """Sertifikat beruvchi tashkilot (masalan, onlayn platforma, universitet)"""
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to="organizations/logos/", blank=True, null=True)

    def __str__(self):
        return self.name

from datetime import datetime

class Certificate(models.Model):
    """Umumiy sertifikat modeli"""
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True, blank=True, null=True)
    certificate_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    qr_code = models.ImageField(upload_to="certificates/qrcodes/", blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        unique_together = ("user", "course")

    def generate_certificate_id(self):
        """Sertifikatni ID sini yaratish"""
        if not self.issue_date:
            self.issue_date = datetime.today().date()  # Hozirgi sanani ishlatish
        return f"CR-{self.course.id}-{self.user.id}-{self.issue_date.strftime('%Y%m%d')}"

    def generate_qr_code(self):
        """Admin tomonidan sozlangan sertifikat URL manzili orqali QR-kod yaratish"""
        site_settings = SiteSettings.objects.first()
        base_url = site_settings.certificate_base_url if site_settings else "https://coding-for-machine.com/certificate/"
        qr_data = f"{base_url}{self.certificate_id}/"
        
        # QR kodini yaratish
        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        self.qr_code.save(f"qr_{self.certificate_id}.png", ContentFile(buffer.getvalue()), save=False)

    def save(self, *args, **kwargs):
        """Sertifikatni saqlash va QR-kodni yaratish"""
        if not self.certificate_id:
            self.certificate_id = self.generate_certificate_id()  # certificate_id ni yaratish
        self.generate_qr_code()  # QR kodni yaratish
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.course.title}"
