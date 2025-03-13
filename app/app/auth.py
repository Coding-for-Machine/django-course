from django.utils.timezone import now
from easyaudit.models import CRUDEvent
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
User = get_user_model()

def get_client_ip(request):
    """Foydalanuvchining haqiqiy IP manzilini olish"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def audit_jwt_login(request, user):
    """JWT login uchun audit log qo‘shish"""
    ip = get_client_ip(request)
    user_content_type = ContentType.objects.get_for_model(User)  # User modelining content type ID-sini olish

    CRUDEvent.objects.create(
        user=user,
        event_type=CRUDEvent.CREATE,  # Login hodisasi uchun CREATE ishlatilmoqda
        datetime=now(),
        object_repr=f"User {user.email} logged in from {ip}",
        object_id=user.id,
        content_type=user_content_type  # <--- **Bu qator qo‘shildi**
    )


def audit_jwt_logout(request, user):
    """JWT logout uchun audit log qo‘shish"""
    ip = get_client_ip(request)
    user_content_type = ContentType.objects.get_for_model(User)  # User modelining content type ID-sini olish
    CRUDEvent.objects.create(
        user=user,
        event_type=CRUDEvent.UPDATE,  # Logout uchun UPDATE ishlatilmoqda
        datetime=now(),
        object_repr=f"User {user.email} logged out from {ip}",
        object_id=user.id,
        content_type=user_content_type
    )

from ninja import Router
from django.contrib.auth import authenticate
from ninja_jwt.tokens import RefreshToken
from django.http import JsonResponse
from pydantic import BaseModel

auth_router = Router()

class LoginSchema(BaseModel):
    email: str
    password: str

@auth_router.post("/token/")
def token_obtain_pair(request, data: LoginSchema):
    user = authenticate(username=data.email, password=data.password)  # Agar USERNAME_FIELD = "email" bo'lsa
    if user is not None:
        refresh = RefreshToken.for_user(user)
        
        # Login audit log
        audit_jwt_login(request, user)
        
        return JsonResponse({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })
    return JsonResponse({"error": "Invalid credentials"}, status=400)


@auth_router.post("/logout/")
def token_blacklist(request, refresh: str):
    try:
        token = RefreshToken(refresh)
        
        # Tokenni qora ro‘yxatga qo‘shish
        if hasattr(token, "blacklist"):
            token.blacklist()
            return JsonResponse({"message": "Logged out successfully"})
        else:
            return JsonResponse({"error": "Token blacklisting is not enabled"}, status=400)

    except Exception as e:
        return JsonResponse({"error": f"Invalid token: {str(e)}"}, status=400)