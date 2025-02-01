import jwt
from datetime import datetime, timedelta
from django.conf import settings

def create_jwt_token(user):
    """ JWT token yaratish """
    payload = {
        "id": user.id,
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(days=1),  # 1 kun amal qiladi
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token
