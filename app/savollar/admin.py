from django.contrib import admin
# from .models import Varyant, Savol
# from django.utils.html import format_html

# # Register your models here.
# class VaryantItem(admin.TabularInline):
#     model = Varyant
#     raw_id_fields = ['savol']

# @admin.register(Savol)
# class OSavolAdmin(admin.ModelAdmin):
    
#     list_display = ['id', "text", "savol_turi", "updated","created"]
#     list_filter = ['id', 'created', 'updated']
#     inlines = [VaryantItem]
#     def book_icon(self, obj):
#         return format_html('<i class="fa fa-book"></i>')  # Book icon qo‘shish
#     book_icon.short_description = 'Icon'