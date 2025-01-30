from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import MyUser, Profile
from savollar.models import Results


@admin.register(MyUser)
class MyUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')  # 'groups' qaytarildi
    filter_horizontal = ('groups', 'user_permissions')  # Bu qator endi to'g'ri ishlaydi 'groups' olib tashlandi

class ProfileAdmin(admin.ModelAdmin):
    list_display=['created_at','bio', 'profile_icon']
    # icon 
    def profile_icon(self, obj):
        return format_html('<i class="fa-regular fa-address-card"></i>')  # Iconni qo‘shish
    profile_icon.short_description = 'Profile-Icon'
admin.site.register(Profile, ProfileAdmin)

admin.site.register(Results)