from django.contrib.admin import TabularInline
from django.contrib import admin
from .models import Lesson, AlgorithmTest, TestCase, Problem, Language
# Register your models here.

admin.site.register(Lesson)
admin.site.register(Language)

# TestCase modelini AlgorithmTest modeliga inline qilish
class TestCaseInline(TabularInline):
    model = TestCase
    extra = 4  # Dastlabki yangi TestCase qo'shishni ko'rsatadi

# AlgorithmTest modelini ro'yxatga olish va inline qo'shish
class AlgorithmTestAdmin(admin.ModelAdmin):
    inlines = [TestCaseInline]

admin.site.register(AlgorithmTest, AlgorithmTestAdmin)

admin.site.register(TestCase) 

admin.site.register(Problem)
