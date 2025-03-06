import os
import environ
from pathlib import Path

# Initialize environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(Path(__file__).resolve().parent.parent, ".env"))

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = env("SECRET_KEY", default="django-insecure-default-key")
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",  
    "channels",        
    "auth_app",        
    "drive",           
    "chat",  
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'assignment.urls'

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

WSGI_APPLICATION = 'assignment.wsgi.application'
ASGI_APPLICATION = 'assignment.asgi.application'

# Google OAuth
GOOGLE_CLIENT_ID = env("GOOGLE_CLIENT_ID", default="")
GOOGLE_CLIENT_SECRET = env("GOOGLE_CLIENT_SECRET", default="")
GOOGLE_AUTH_REDIRECT_URI = env("GOOGLE_AUTH_REDIRECT_URI", default="http://localhost:8000/auth/callback/")
GOOGLE_AUTH_SCOPE = env.list("GOOGLE_AUTH_SCOPE", default=["openid", "email", "profile"])

# Google Drive API
GOOGLE_API_KEY = env("GOOGLE_API_KEY", default="")
GOOGLE_DRIVE_SCOPES = env.list("GOOGLE_DRIVE_SCOPES", default=["https://www.googleapis.com/auth/drive.file"])

# Paths to Credentials JSON Files
GOOGLE_OAUTH_CREDENTIALS = os.path.join(BASE_DIR, env("GOOGLE_OAUTH_CREDENTIALS", default="assignment/credential/Oauth.json"))
GOOGLE_SERVICE_ACCOUNT_CREDENTIALS = os.path.join(BASE_DIR, env("GOOGLE_SERVICE_ACCOUNT_CREDENTIALS", default="assignment/credential/service_acc.json"))

# Redis WebSockets (For Render, use Redis URL)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [env("REDIS_URL", default=("127.0.0.1", 6379))],
        },
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
