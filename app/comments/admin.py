from django.contrib import admin

# Register your models here.

from .models import Comments

class CommentAdmin(admin.ModelAdmin):
    list_display = ["user__email", "problems__title", "comments", 'created_at', "updated_at"]
    list_display_links = ['comments']
    list_filter = ['comments', 'updated_at', 'created_at']


admin.site.register(Comments, CommentAdmin)