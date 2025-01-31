from django.contrib import admin
from django.utils.html import format_html
from .models import (
    UserActivityDaily, Badge, UserBadge, 
    UserActivitySummary, UserLeaderboard, 
    UserLessonStatus, UserProblemStatus
)

# ==========================
# 1. UserActivityDaily modeli uchun admin
# ==========================
@admin.register(UserActivityDaily)
class UserActivityDailyAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'activity_count', 'total_duration', 'score')
    list_filter = ('date',)
    search_fields = ('user__email',)
    ordering = ('-date',)


# ==========================
# 2. Nishonlar (Badge) uchun admin
# ==========================
@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'icon_preview')
    search_fields = ('name',)
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html(f'<img src="{obj.icon.url}" width="50" height="50" style="border-radius: 5px;" />')
        return "-"
    icon_preview.short_description = "Icon Preview"


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'date_earned')
    list_filter = ('badge', 'date_earned')
    search_fields = ('user__email', 'badge__name')


# ==========================
# 3. UserActivitySummary uchun admin
# ==========================
@admin.register(UserActivitySummary)
class UserActivitySummaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'period_type', 'period_start', 'period_end', 'total_score', 'total_activity')
    list_filter = ('period_type', 'period_start')
    search_fields = ('user__email',)


# ==========================
# 4. Reyting (Leaderboard) uchun admin
# ==========================
@admin.register(UserLeaderboard)
class UserLeaderboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_score', 'last_updated')
    search_fields = ('user__email',)
    ordering = ('-total_score',)


# ==========================
# 5. UserLessonStatus uchun admin
# ==========================
@admin.register(UserLessonStatus)
class UserLessonStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'is_completed', 'progress')
    list_filter = ('is_completed',)
    search_fields = ('user__email', 'lesson__title')
    ordering = ('-progress',)


# ==========================
# 6. UserProblemStatus uchun admin
# ==========================
@admin.register(UserProblemStatus)
class UserProblemStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'is_completed', 'score')
    list_filter = ('is_completed',)
    search_fields = ('user__email', 'problem__title')
    ordering = ('-score',)
