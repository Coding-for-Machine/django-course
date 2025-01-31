from django.contrib import admin
from .models import Course, Enrollment, Payment, Module
from django.utils.text import slugify

# Course Admin
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'price', 'lesson_count', 'unlisted', 'created_at', 'updated_at')
    search_fields = ('title', 'slug')
    list_filter = ('unlisted',)  # Filtrlar qo'shish
    prepopulated_fields = {'slug': ('title',)}  # Slugni avtomatik yaratish

    def save_model(self, request, obj, form, change):
        """
        Kursni saqlashdan oldin slugni sozlash va lesson_count ni hisoblash.
        """
        if not obj.slug:
            obj.slug = slugify(obj.title)  # Slugni `title` asosida yaratish
        if not obj.lesson_count:
            obj.lesson_count = obj.modules.aggregate(models.Count('lessons'))['lessons__count']
        obj.save()

admin.site.register(Course, CourseAdmin)


# Enrollment Admin
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at', 'is_paid', 'created_at', 'updated_at')
    search_fields = ('user__username', 'course__title')
    list_filter = ('is_paid',)

admin.site.register(Enrollment, EnrollmentAdmin)


# Payment Admin
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'amount', 'payment_status', 'payment_date')
    search_fields = ('enrollment__user__username', 'enrollment__course__title')
    list_filter = ('payment_status',)

admin.site.register(Payment, PaymentAdmin)


# Module Admin
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'slug', 'created_at', 'updated_at')
    search_fields = ('title', 'course__title', 'slug')
    list_filter = ('course',)
    prepopulated_fields = {'slug': ('title',)}  # Slugni avtomatik yaratish

    def save_model(self, request, obj, form, change):
        """
        Modulni saqlashdan oldin slugni sozlash.
        """
        if not obj.slug:
            obj.slug = slugify(obj.title)  # Slugni `title` asosida yaratish
        obj.save()

admin.site.register(Module, ModuleAdmin)
