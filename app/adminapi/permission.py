from ninja.security import HttpBearer
from django.contrib.auth.models import Permission

class HasSpecificPermission(HttpBearer):
    """
    Foydalanuvchida specific permission borligini tekshiradi.
    """
    def __init__(self, permission_codename):
        self.permission_codename = permission_codename

    def authenticate(self, request, token):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm(f"app.{self.permission_codename}")

class IsInPrimaryGroup(HttpBearer):
    """
    Foydalanuvchi o‘zining asosiy guruhiga tegishli API-larga kira olishi mumkin.
    """
    def authenticate(self, request, token):
        return request.user.is_authenticated and request.user.primary_group is not None

class HasSupplementaryGroup(HttpBearer):
    """
    Foydalanuvchi qo‘shimcha guruhlaridagi ruxsatlardan foydalanishi mumkin.
    """
    def authenticate(self, request, token):
        return request.user.is_authenticated and request.user.supplementary_groups.exists()

class IsStaff(HttpBearer):
    def authenticate(self, request, token):
        return request.user.is_authenticated and request.user.is_staff

class IsSuperuser(HttpBearer):
    def authenticate(self, request, token):
        return request.user.is_authenticated and request.user.is_superuser

class IsInGroup(HttpBearer):
    def __init__(self, group_name):
        self.group_name = group_name

    def authenticate(self, request, token):
        return request.user.is_authenticated and request.user.groups.filter(name=self.group_name).exists()
