import os
from pathlib import Path
from django import apps
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv
from core.settings.jazzmin import JAZZMIN_SETTINGS
from celery.schedules import crontab, timedelta 

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

IS_PRODUCTION = os.getenv("PRODUCTION", "False").lower() == "true"

if IS_PRODUCTION:
    from core.settings.production import *
else:
    from core.settings.development import *

THEME_APPS = [
    'jazzmin',
]

MY_APPS = [
    'apps.testapp',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LIBRARY_APPS = [
    'rest_framework',
    'drf_yasg',
    'django_ckeditor_5',
    'modeltranslation',
    "corsheaders",
]

INSTALLED_APPS = [
    *THEME_APPS,
    *DJANGO_APPS,
    *LIBRARY_APPS,
    *MY_APPS,
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'



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


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LANGUAGES = [
    ('ru', _('Russian')),
    ('ky', _('Kyrgyz')),
    ('en', _('English')),
]


MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
MODELTRANSLATION_CUSTOM_FIELDS = ('CKEditor5Field',)


MEDIA_URL = '/back_media/'
MEDIA_ROOT = BASE_DIR / 'back_media/'


STATIC_URL = '/back_static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'back_static')


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}


CKEDITOR_5_CONFIGS = {
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3', 
            '|', 'bulletedList', 'numberedList', 'alignment'
        ],
        'toolbar': [
            'heading', '|', 
            'bold', 'italic', 'underline', 'strikethrough', 'code', '|',
            'fontSize', 'fontColor', 'fontBackgroundColor', '|',
            'link', 'imageUpload', 'mediaEmbed', 'insertTable', 'blockQuote', '|',
            'alignment', 'outdent', 'indent', '|',
            'sourceEditing', 'removeFormat'
        ],
        'upload_url': '/ckeditor5/image_upload/',
        'heading': {
            'options': [
                { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
                { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
                { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
                { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
            ]
        },
        'table': {
            'contentToolbar': [
                'tableColumn', 'tableRow', 'mergeTableCells', 
                'tableProperties', 'tableCellProperties'
            ]
        },
        'image': {
            'toolbar': [
                'imageTextAlternative', '|', 
                'imageStyle:alignLeft', 'imageStyle:alignCenter', 'imageStyle:alignRight', '|',
                'imageStyle:full', 'imageStyle:side'
            ]
        }
    },
    'minimal': {
        'toolbar': ['bold', 'italic', 'link'],
    },
}

# # 2. Настройки SimpleJWT (указываем lifetimes и поле email)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Токен живёт 1 час
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),     # Рефреш живёт 1 день
    'AUTH_HEADER_TYPES': ('Bearer',),                # В заголовке пишем Bearer <token>
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
} 

# --- REDIS CACHE (Используем DB 1) ---
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.getenv("REDIS_URL", "redis://127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        } 
    }
}


# Где лежат очереди задач (Redis как Broker)
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")

# Где сохранять результаты выполнения (Redis как Result Backend)
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")

# Формат передачи данных (JSON — стандарт)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Bishkek'


CELERY_BEAT_SCHEDULE = {
    # Задача 1: Запускается каждые 5 минут
    'run-stats-every-5-minutes': {
        'task': 'apps.testapp.tasks.monthly_user_stats_task',
        'schedule': 300.0, # Каждые 300 секунд
    }, 
    
    # Задача 2: Запускается каждый день в 00:00 (Полезно для рассылок/отчетов)
    'run-daily-midnight-task': {
        'task': 'apps.testapp.tasks.monthly_user_stats_task',
        'schedule': crontab(hour=0, minute=0),
    }, 


    'clear-expired-cache-every-minute': {
        'task': 'apps.testapp.tasks.clear_expired_cache_task',
        'schedule': 60.0,  # Каждую минуту 
    },
} 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'my_database'),
        'USER': os.environ.get('DB_USER', 'my_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'my_password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Настройка кэширования Redis
REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Настройки Celery
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Расписание Celery Beat
CELERY_BEAT_SCHEDULE = {
    'clear-expired-cache-every-minute': {
        'task': 'api.tasks.clear_expired_cache_task',
        'schedule': 60.0,
    },
} 