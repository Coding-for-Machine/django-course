from django.contrib import admin
from .models import Course, Enrollment, Payment, MyModules
from django.utils.text import slugify

# Course Admin
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'price', 'lesson_count', 'unlisted', 'created_at', 'updated_at')
    search_fields = ('title', 'slug')
    list_filter = ('unlisted',)
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        """
        Kursni saqlashdan oldin slugni sozlash va lesson_count ni hisoblash.
        """
        if not obj.slug:
            obj.slug = slugify(obj.title)

        super().save_model(request, obj, form, change)  # Avval kursni saqlaymiz

        # Modullarni va darslarni hisoblash
        obj.lesson_count = sum(module.lesson.count() for module in obj.modules.all())
        
        super().save_model(request, obj, form, change)  # Yana saqlaymiz, lesson_count yangilanishi uchun

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
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        """
        Modulni saqlashdan oldin slugni sozlash.
        """
        if not obj.slug:
            obj.slug = slugify(obj.title)
        
        super().save_model(request, obj, form, change)  # Avval modulni saqlaymiz

admin.site.register(MyModules, ModuleAdmin)
