# Course Platform - Django & PostgreSQL

**42.uz ga o‘xshagan kurs platformasi**  
Django va PostgreSQL asosida kurslar yaratish, boshqarish va foydalanuvchilarni ro‘yxatdan o‘tkazish imkonini beruvchi tizim.
DataBase Url--> https://www.drawdb.app/editor?shareId=e6780827401c08519b0fe845f28622c8
## 📌 Xususiyatlari:
- **Foydalanuvchilar tizimi** (O‘qituvchi, O‘quvchi, Admin)
- **Kurslarni yaratish va boshqarish**
- **Video va hujjatlarni yuklash**
- **Django va Ninja REST API bilan backend**
- **PostgreSQL asosida optimallashtirilgan ma’lumotlar bazasi**
- **Docker yordamida deploy qilish imkoniyati**
- **JWT Token orqali autentifikatsiya**

## 🛠 Texnologiyalar:
- **Backend:** Django, Django-Ninja
- **Ma’lumotlar bazasi:** PostgreSQL yoki Sqlite
- **Keshlash:** Redis
- **Deploy:** Docker, Nginx, Gunicorn
- **Versiya nazorati:** Git, GitHub

## 🔧 O‘rnatish:

1. **Repodan nusxa olish:**
   ```bash
   git clone https://github.com/Coding-for-Machine/django-course.git
   cd django-course


### 2️⃣ Virtual muhit yaratish va faollashtirish:
```bash
python -m venv venv
source venv/bin/activate  # MacOS/Linux
echo "Virtual muhit faollashtirildi!"
```
Windows uchun:
```bash
venv\Scripts\activate  
echo "Virtual muhit faollashtirildi!"
```

### 3️⃣ Kerakli kutubxonalarni o‘rnatish:
```bash
pip install -r requirements.txt
echo "Barcha kerakli kutubxonalar o‘rnatildi!"
```

### 4️⃣ Ma’lumotlar bazasini sozlash:
`.env` faylini yaratib, quyidagi sozlamalarni qo‘shing:
```bash
echo "DB_NAME=course_db" >> .env
echo "DB_USER=postgres" >> .env
echo "DB_PASSWORD=yourpassword" >> .env
echo "DB_HOST=localhost" >> .env
echo "DB_PORT=5432" >> .env
echo ".env fayli yaratildi!"
```

### 5️⃣ Ma’lumotlar bazasini yaratish:
```bash
python manage.py migrate
echo "Ma’lumotlar bazasi migratsiya qilindi!"
```

### 6️⃣ Admin foydalanuvchi yaratish:
```bash
python manage.py createsuperuser
```

### 7️⃣ Serverni ishga tushirish:
```bash
python manage.py runserver
redis-server --port 6380
echo "Server ishga tushdi! http://127.0.0.1:8000"
```

## 📂 API Endpointlar

- **Kurslar ro‘yxatini olish** → `GET /api/courses/`
- **Yangi kurs yaratish** → `POST /api/courses/`
- **Foydalanuvchi ro‘yxatdan o‘tishi** → `POST /api/user/register`
  ![image](https://github.com/user-attachments/assets/c06cff8f-6487-4d63-afbc-8c24b38de8f5)

- **Login qilish** → `POST /api/user/login/`
![image](https://github.com/user-attachments/assets/20e5eca4-20c0-4d70-a0e7-4a232efe7754)

---
## 🚀 Deploy qilish (Docker bilan)

### 1️⃣ Docker imajni yaratish va konteynerni ishga tushirish:
```bash
docker-compose up --build -d
echo "Docker konteynerlari ishga tushdi!"
```

### 2️⃣ Admin panelga kirish:
```bash
echo "Admin paneliga kirish uchun: http://localhost:8000/admin"
```


## 👨‍💻 Loyiha muallifi:
- **Ism:** Asadbek  
- **LinkedIn:** [Profil](https://www.linkedin.com/in/coding-for-machine)  
- **GitHub:** [Profil](https://github.com/Coding-for-Machine)  

