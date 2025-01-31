from django.contrib import admin
from django.utils.html import format_html
from .models import SiteSettings, Organization, Certificate

# Sayt Sozlamalari
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('certificate_base_url',)
    search_fields = ('certificate_base_url',)

admin.site.register(SiteSettings, SiteSettingsAdmin)


# Tashkilotlarni boshqarish
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'logo_tag')
    search_fields = ('name', 'website')

    def logo_tag(self, obj):
        """Tashkilot logotipini admin panelida ko'rsatish"""
        if obj.logo:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.logo.url)
        return '-'
    logo_tag.short_description = 'Logo'


admin.site.register(Organization, OrganizationAdmin)


# Sertifikatlarni boshqarish
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_id', 'user', 'course', 'issue_date', 'slug', 'view_qr_code')
    list_filter = ('course', 'issue_date', 'user')
    search_fields = ('certificate_id', 'user__email', 'course__title',)
    readonly_fields = ('certificate_id', 'qr_code', 'slug')
    actions = ['generate_qr_for_selected']

    def generate_qr_for_selected(self, request, queryset):
        """Tanlangan sertifikatlar uchun QR kodlarini avtomatik yaratish"""
        for certificate in queryset:
            certificate.generate_qr_code()
            certificate.save()
        self.message_user(request, "QR kodlari muvaffaqiyatli yaratildi.")

    generate_qr_for_selected.short_description = "Tanlangan sertifikatlar uchun QR kodini yaratish"

    def view_qr_code(self, obj):
        """QR kodini admin panelida ko'rsatish"""
        if obj.qr_code:
            return format_html('<img src="{}" style="width: 100px; height: 100px;" />', obj.qr_code.url)
        return '-'
    view_qr_code.short_description = 'QR Kod'


admin.site.register(Certificate, CertificateAdmin)
