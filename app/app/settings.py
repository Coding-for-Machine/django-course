from datetime import timedelta
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-dtqls^u%s0*-+#x5w94d9qveq$f)jjap$ep$tzfstd#k9ps$5#'


DEBUG = True

ALLOWED_HOSTS = ['*', '185.213.230.160']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #  my apps
    'courses.apps.CoursesConfig',
    'lessons.apps.LessonsConfig',
    'users.apps.UsersConfig',
    'userstatus.apps.UserstatusConfig',
    'savollar.apps.SavollarConfig',
    'comments.apps.CommentsConfig',
    'solution.apps.SolutionConfig',
    'Certificate.apps.CertificateConfig',
    'grade.apps.GradeConfig',

    # Boshqa app'lar
    # loglarni kuzatish
    'easyaudit',
    "django_extensions",
    'corsheaders',
    'django_ckeditor_5',
    'ninja_jwt',
    'ninja_extra',
    'ninja_jwt.token_blacklist',
]

AUTH_USER_MODEL = "users.MyUser"

CORS_ALLOW_ALL_ORIGINS = True 

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # log
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
]


# JWT sozlamalari
NINJA_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),  
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY + "asadbek123456789",
    'AUTH_HEADER_TYPES': ('Bearer',),
    "BLACKLIST_AFTER_ROTATION": True,  
}

#  ---------------------------------
#  Redis Cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6380/1",  # Redis serverga ulanish
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",  # Redis bilan ishlash uchun
        }
    }
}

#  ---------------------------------
ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#database
# bu nvim da qilinayapdi

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent' 

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Statik fayllarni yig'ish uchun

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


customColorPalette = [

        {

            'color': 'hsl(4, 90%, 58%)',

            'label': 'Red'

        },

        {

            'color': 'hsl(340, 82%, 52%)',

            'label': 'Pink'

        },

        {

            'color': 'hsl(291, 64%, 42%)',

            'label': 'Purple'

        },

        {

            'color': 'hsl(262, 52%, 47%)',

            'label': 'Deep Purple'

        },

        {

            'color': 'hsl(231, 48%, 48%)',

            'label': 'Indigo'

        },

        {

            'color': 'hsl(207, 90%, 54%)',

            'label': 'Blue'

        },

    ]




CKEDITOR_5_FILE_STORAGE = 'app.store.CkeditorCustomStorage'
CKEDITOR_5_CUSTOM_CSS = None
CKEDITOR_5_CONFIGS = {

    'default': {

        'toolbar': ['heading', '|', 'bold', 'italic', 'link',

                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],



    },

    'extends': {

        'blockToolbar': [

            'paragraph', 'heading1', 'heading2', 'heading3',

            '|',

            'bulletedList', 'numberedList',

            '|',

            'blockQuote',

        ],

        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',

        'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',

                    'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',

                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',

                    'insertTable',],

        'image': {

            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',

                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],

            'styles': [

                'full',

                'side',

                'alignLeft',

                'alignRight',

                'alignCenter',

            ]



        },

        'table': {

            'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',

            'tableProperties', 'tableCellProperties' ],

            'tableProperties': {

                'borderColors': customColorPalette,

                'backgroundColors': customColorPalette

            },

            'tableCellProperties': {

                'borderColors': customColorPalette,

                'backgroundColors': customColorPalette

            }

        },

        'heading' : {

            'options': [

                { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },

                { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },

                { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },

                { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }

            ]

        }

    },

    'list': {

        'properties': {

            'styles': 'true',

            'startIndex': 'true',

            'reversed': 'true',

        }

    }

}
# CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff" 
CKEDITOR_5_FILE_UPLOAD_PERMISSIONS = "staff"