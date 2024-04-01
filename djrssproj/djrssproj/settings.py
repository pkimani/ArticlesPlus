# settings.py
import os
from pathlib import Path
from kombu import Exchange, Queue
from corsheaders.defaults import default_headers
from rssapp.log_handlers import UniqueFileHandler  # Import the custom log handler

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '[::1]', '0.0.0.0']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rssapp.apps.RssappConfig',
    'rest_framework',
    'corsheaders',
    'celery',
    'django_celery_results',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djrssproj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'djrssproj.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'articles_db',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
        },
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'rssapp.log_handlers.UniqueFileHandler',  # Use the custom handler
            'directory': '/home/pkimani/getting-started-app/djrssproj/Logs',  # Directory where logs will be stored
            'filename': 'django',  # Base filename for the logs
            'maxBytes': 262144000,  # 250MB
            'backupCount': 0,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Celery settings
USE_CELERY = True
CELERY_BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_TASK_QUEUES = (
    Queue('celery', Exchange('celery'), routing_key='celery', queue_arguments={'x-max-priority': 5}),
)

# CORS settings
CORS_ORIGIN_WHITELIST = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://localhost:8000',
    'https://127.0.0.1:8000'
]

CORS_ALLOW_HEADERS = list(default_headers) + ['Timezone']

# HTTPS settings
SECURE_HSTS_SECONDS = 3600
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Custom settings
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPML_FILE_PATH = os.path.join(BASE_DIR, 'XML', 'Feeds.opml')
PROMPT = 'Please score the given article titles from 1 to 100 based on their significance and create a JSON dictionary named "articles" with a list of objects containing "id" and "score". The "id" is a 32-character hash code, and the "score" is the significance score. For each title listed after "TITLES:", create a JSON object with "id" and "score". The title is between the first backticks, and the hash code "id" is within the second backticks per line. Exclude the title from the JSON output, only include the hash code "id" and its score. The output should be the "articles" JSON dictionary with objects holding the hash code "id" and the ranking score "score" for each title.\nSignificance criteria:\n1. Score 100 for critical events and emergencies.\n2. Score 90 for topics on Africa, Africans, and the Black diaspora.\n3. Score 80 for exceptional STEM advancements.\n4. Score 75 for climate change, ecology, and environmentalism.\n5. Score 40 for sports.\n6. Score 20 for entertainment and media personalities.\n7. Score 0 for retail discounts and online shopping promotions, excluding new product launches.\nFor unmentioned categories, assign a general score without commentary, only provide the JSON response.\nExample Response:\n```json\n{"articles": [{"id": "29d5f5684f8ceb75c2ad66d968be8cd0", "score": 80}, {"id": "b39b55460cbe71b7940fe9043750e86b", "score": 20}]}```\nTITLES:'