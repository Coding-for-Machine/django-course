from django.contrib.admin import TabularInline
from django.contrib import admin
from .models import Language, Lesson, Problem, Function, AlgorithmTest, TestCase
from django.utils.html import format_html


# Language Admin
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'id')  # Ko'rsatiladigan ustunlar
    search_fields = ('name', 'slug')  # Qidiruvni faollashtirish
    list_filter = ('name',)  # Filtrlar qo'shish
    prepopulated_fields = {'slug': ('name',)}  # Slugni avtomatik to'ldirish

admin.site.register(Language, LanguageAdmin)


# Lesson Admin
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'lesson_type', 'locked', 'preview', 'created_at', 'slug')
    search_fields = ('title', 'module__title')  # Qidiruvni faollashtirish
    list_filter = ('lesson_type', 'locked', 'preview')
    prepopulated_fields = {'slug': ('title',)}  # Slugni avtomatik to'ldirish

admin.site.register(Lesson, LessonAdmin)


# Problem Admin
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'difficulty', 'slug', 'created_at')
    search_fields = ('title', 'lesson__title', 'difficulty')
    list_filter = ('difficulty', 'lesson')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Problem, ProblemAdmin)


# Function Admin
class FunctionAdmin(admin.ModelAdmin):
    list_display = ('language', 'problem', 'function', 'created_at')
    search_fields = ('language__name', 'problem__title', 'function')
    list_filter = ('language', 'problem')

admin.site.register(Function, FunctionAdmin)



class TestCaseInline(TabularInline):
    model = TestCase
    extra = 4  # Dastlabki yangi TestCase qo'shishni ko'rsatadi

# AlgorithmTest modelini ro'yxatga olish va inline qo'shish
class AlgorithmTestAdmin(admin.ModelAdmin):
    list_display = ('language', 'problem', 'algorithm', 'created_at')
    search_fields = ('language__name', 'problem__title', 'algorithm')
    list_filter = ('language', 'problem')
    inlines = [TestCaseInline]

admin.site.register(AlgorithmTest, AlgorithmTestAdmin)






