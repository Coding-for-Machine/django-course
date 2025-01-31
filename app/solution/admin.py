from django.contrib import admin
from .models import Solution, UserQuizResult, UserQuestionResult

# ==============================
# 1️⃣ Solution (Foydalanuvchi Yechimi)
# ==============================
@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'language', 'is_accepted', 'score', 'execution_time', 'memory_usage', 'created_at')
    search_fields = ('user__email', 'problem__title', 'language__name')
    list_filter = ('is_accepted', 'language')
    readonly_fields = ('created_at', 'updated_at', 'score')

    def get_queryset(self, request):
        """Natijalarni vaqt bo‘yicha kamayish tartibida chiqarish"""
        return super().get_queryset(request).order_by('-created_at')


# ==============================
# 2️⃣ UserQuizResult (Foydalanuvchi Quiz Natijalari)
# ==============================
@admin.register(UserQuizResult)
class UserQuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'correct_answers', 'total_questions', 'completed_at')
    search_fields = ('user__email', 'quiz__title')
    list_filter = ('completed_at',)
    readonly_fields = ('completed_at',)

    def get_queryset(self, request):
        """Natijalarni eng yuqori ball bo‘yicha saralash"""
        return super().get_queryset(request).order_by('-score')


# ==============================
# 3️⃣ UserQuestionResult (Foydalanuvchi Savol Natijalari)
# ==============================
@admin.register(UserQuestionResult)
class UserQuestionResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'is_correct', 'answered_at')
    search_fields = ('user__email', 'question__text')
    list_filter = ('is_correct', 'answered_at')
    readonly_fields = ('answered_at',)

    def get_queryset(self, request):
        """Yaqinda javob berilgan natijalarni birinchi chiqarish"""
        return super().get_queryset(request).order_by('-answered_at')
