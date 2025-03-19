from django.contrib.admin import TabularInline
from django.contrib import admin
from .models import Language, Lesson, Problem, Function, TestCase
from django.utils.html import format_html


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'id')  
    search_fields = ('name', 'slug')  
    list_filter = ('name',)  
    prepopulated_fields = {'slug': ('name',)}  

admin.site.register(Language, LanguageAdmin)


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'lesson_type', 'preview', 'created_at', 'slug')
    search_fields = ('title', 'module__title') 
    list_filter = ('lesson_type', 'preview')
    prepopulated_fields = {'slug': ('title',)} 

admin.site.register(Lesson, LessonAdmin)

class TestCaseInline(TabularInline):
    model = TestCase
    extra = 4 

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'difficulty', 'slug', 'created_at')
    search_fields = ('title', 'lesson__title', 'difficulty')
    list_filter = ('difficulty', 'lesson')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TestCaseInline]

admin.site.register(Problem, ProblemAdmin)



class FunctionAdmin(admin.ModelAdmin):
    list_display = ('language', 'problem', 'function', 'created_at')
    search_fields = ('language__name', 'problem__title', 'function')
    list_filter = ('language', 'problem')

admin.site.register(Function, FunctionAdmin)