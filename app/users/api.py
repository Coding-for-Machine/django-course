from ninja import Router
from ninja_jwt.authentication import JWTAuth
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from ninja_jwt.tokens import RefreshToken

from .models import MyUser
from .schemas import UserRegisterSchema, UserSchema, UserLoginSchema

# Router yaratamiz
user_router = Router()

# Ro‘yxatdan o‘tish (Register)
@user_router.post("/register", response={201: UserSchema, 400: str})
def register(request, data: UserRegisterSchema):
    if MyUser.objects.filter(email=data.email).exists():
        return 400, "Email already exists"
    
    # Foydalanuvchi yaratish
    user = MyUser.objects.create(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        password=make_password(data.password)  # Parolni hash qilish
    )

    return 201, user

# Login qilish
@user_router.post("/login", response={200: dict, 401: str})
def login(request, data: UserLoginSchema):
    user = MyUser.objects.filter(email=data.email).first()
    
    if not user or not check_password(data.password, user.password):
        return 401, "Email or password incorrect"
    
    # JWT token yaratish
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }

# Profilni olish (faqat login qilgan foydalanuvchilar)
@user_router.get("/profile", response={200: UserSchema, 401: str}, auth=JWTAuth())
def get_profile(request):
    user = request.auth  # JWT orqali foydalanuvchi aniqlanadi
    return 200, user
