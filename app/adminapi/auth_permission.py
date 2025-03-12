from django.contrib.auth.models import Permission
from ninja_jwt.authentication import JWTAuth
from ninja.security import HttpBearer


class JWTBaseAuth(HttpBearer):
    """`JWTAuth` bilan autentifikatsiya qiluvchi bazaviy klass."""
    
    def authenticate(self, request, token):
        jwt_auth = JWTAuth()
        user = jwt_auth.authenticate(request, token)

        if user and user.is_authenticated:
            request.user = user
            return user
        return None


class HasSpecificPermission(JWTBaseAuth):
    """Foydalanuvchida berilgan permission bormi, tekshiradi."""
    
    def __init__(self, permission_codename):
        self.permission_codename = permission_codename

    def authenticate(self, request, token):
        user = super().authenticate(request, token)
        return user if user and user.has_perm(self.permission_codename) else None


class IsInGroup(JWTBaseAuth):
    """Foydalanuvchi berilgan guruhga tegishli ekanligini tekshiradi."""
    
    def __init__(self, group_name):
        self.group_name = group_name

    def authenticate(self, request, token):
        user = super().authenticate(request, token)
        return user if user and user.groups.filter(name=self.group_name).exists() else None


class IsSuperuser(JWTBaseAuth):
    """Foydalanuvchi `superuser` ekanligini tekshiradi."""
    
    def authenticate(self, request, token):
        user = super().authenticate(request, token)
        return user if user and user.is_superuser else None


class IsStaff(JWTBaseAuth):
    """Foydalanuvchi `staff` ekanligini tekshiradi."""
    
    def authenticate(self, request, token):
        user = super().authenticate(request, token)
        return user if user and user.is_staff else None


class IsInPrimaryGroup(JWTBaseAuth):
    """Foydalanuvchi asosiy guruhiga tegishli ekanligini tekshiradi."""
    
    def authenticate(self, request, token):
        user = super().authenticate(request, token)
        return user if user and getattr(user, "primary_group", None) else None


class HasSupplementaryGroup(JWTBaseAuth):
    """Foydalanuvchi qo‘shimcha guruhlaridagi ruxsatlardan foydalanishi mumkinligini tekshiradi."""
    
    def authenticate(self, request, token):
        user = super().authenticate(request, token)
        return user if user and getattr(user, "supplementary_groups", None) else None
