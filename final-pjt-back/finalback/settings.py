"""
Django settings for finalback project.

Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# secret key 호출을 위해 import
import os, json
from django.core.exceptions import ImproperlyConfigured 


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # local apps
    'accounts',
    'movies',
    'community',

    # 3rd party apps
    'django_extensions',
    'corsheaders', # CORS 세팅
    'rest_framework',
    'rest_framework.authtoken', # token 기반 auth

    # django all auth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', # allauth google
    'allauth.socialaccount.providers.kakao', # allauth KaKao

    # DRF auth
    'dj_rest_auth', # sign 제외 auth 관련 담당
    'dj_rest_auth.registration', # signup 담당

    # native apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # dj-rest-auth signup 필요
    'django.contrib.sites',
]

SITE_ID = 1

# 회원가입 재정의
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'accounts.serializers.account.AccountSignUpSerializer',
}

# 사용자 정보 조회 재정의
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER' : 'accounts.serializers.account.ProfileSerializer'
}

ACCOUNT_ADAPTER = 'accounts.adapters.CustomAccountAdapter'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # 반드시 CommonMiddleware보다 위에 위치
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'finalback.urls'

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

WSGI_APPLICATION = 'finalback.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 내장 User 모델을 재정의한 User 모델을 사용하도록 변경
# Custom user model 정의 후 대체 
AUTH_USER_MODEL = 'accounts.User'


# 특정 origin 에게만 교차 출처 허용
# CORS_ALLOWED_ORIGINS = [
#     # Vue LocalHost
#     'http://localhost:8080',

#     'http://127.0.0.1:8001'
# ]

# 모두에게 교차 출처 허용(*)
CORS_ALLOW_ALL_ORIGINS = True

# SITE_ID = 1 # django.contrib.sites

REST_FRAMEWORK = {
    # 기본 인증 방식 설정(Basic TokenAuthentication)
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],

    # 기본 권한 설정
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated', # 인증받은 자에게 권한 허용
        # 'rest_framework.permissions.AllowAny', # 모두에게 권한 허용
    ]
}



# secret key 호출
secret_file = os.path.join(BASE_DIR, 'secrets.json') #secrets.json을 불러옴

with open(secret_file, 'r') as f: #open as로 secret.json을 열어줍니다.
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets): #예외 처리를 통해 오류 발생을 검출합니다.
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret("SECRET_KEY")

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]