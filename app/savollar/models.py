from django.db import models
from users.models import MyUser
from lessons.models import Problem, Lesson
from django.contrib.auth.models import User
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
        return str(self.text)
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
        return f"{self.savol.text} tugri_yoke_natugri:{self.text} xato yoke trug\'risi {self.tugri_yoke_natugri}"

class Results(models.Model):
    quiz=models.ForeignKey(Savol, on_delete=models.CASCADE)
    user=models.ForeignKey(MyUser, on_delete=models.CASCADE)
    javob = models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)
    
    class Meta:
        verbose_name = "Javoblar"
        verbose_name_plural = "Javoblar"