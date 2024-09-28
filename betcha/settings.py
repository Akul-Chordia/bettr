"""
Django settings for betcha project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-v!!)8l*7jsn&i4l1zy1l31s!f=qpfizmb+%5&$wksc)=_dig=5"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin" ,
    "django.contrib.auth" ,
    "django.contrib.contenttypes" ,
    "django.contrib.sessions" ,
    "django.contrib.messages" ,
    "django.contrib.staticfiles" ,
    "bets"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware" ,
    "django.contrib.sessions.middleware.SessionMiddleware" ,
    "django.middleware.common.CommonMiddleware" ,
    "django.middleware.csrf.CsrfViewMiddleware" ,
    "django.contrib.auth.middleware.AuthenticationMiddleware" ,
    "django.contrib.messages.middleware.MessageMiddleware" ,
    "django.middleware.clickjacking.XFrameOptionsMiddleware" ,
]

ROOT_URLCONF = "betcha.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates" ,
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True ,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug" ,
                "django.template.context_processors.request" ,
                "django.contrib.auth.context_processors.auth" ,
                "django.contrib.messages.context_processors.messages" ,
            ] ,
        } ,
    } ,
]

WSGI_APPLICATION = "betcha.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3" ,
        "NAME": BASE_DIR / "db.sqlite3" ,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator" ,
    } ,
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator" ,
    } ,
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator" ,
    } ,
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator" ,
    } ,
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

DATE_INPUT_FORMATS = ['%d-%m-%Y']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static" ,
]

STRIPE_TEST_PUBLIC_KEY = 'pk_test_51Q3juAH1XCaiLE9lF5AcoguX3t5QTm7AfgCUpVFYaFhpC0Wz0koTfi4WUMcCFj7OgxHjK6FuamnIO9DL75wnvaYc00HuxLSuDL'
STRIPE_TEST_SECRET_KEY = 'sk_test_51Q3juAH1XCaiLE9lrMm5gnGDe2MIOzs1ZTPOVNGKGsCbcOCHZaAkpEEeTyryhvHA373yajvj8ruRRlKJGlpu0vlE00FVhnos8x'
EMAIL_USER = 'betcha.donotreply.official@gmail.com'
APP_PASS = 'ergf prol hdek duhr'