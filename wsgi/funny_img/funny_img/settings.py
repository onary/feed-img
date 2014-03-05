"""
Django settings for funny_img project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

OPENSHIFT = os.environ.has_key('OPENSHIFT_APP_NAME')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'aaq8z5%00+9s^c(4qbg0q7my+4nub#4qe0h9%q_&u68@h%6fx-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "apps.worker",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'funny_img.urls'

WSGI_APPLICATION = 'funny_img.wsgi.application'


# Database
if OPENSHIFT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['OPENSHIFT_APP_NAME'],
            'USER': os.environ['OPENSHIFT_MYSQL_DB_USERNAME'],
            'PASSWORD': os.environ['OPENSHIFT_MYSQL_DB_PASSWORD'],
            'HOST': os.environ['OPENSHIFT_MYSQL_DB_HOST'],
            'PORT': os.environ['OPENSHIFT_MYSQL_DB_PORT'],
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "imgdb",
            "USER": "img",
            "PASSWORD": "img",
            "HOST": "",
            "PORT": "",
        }
    }
# Redis settings for cache, sessions and templates bytecode
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_DB = 1
REDIS_PASSWORD = ''
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = ''
STATIC_ROOT = ''

if OPENSHIFT:
    MEDIA_ROOT = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR'), 'wsgi', 'media')
    STATIC_ROOT = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR'), 'wsgi', 'static')

    # Redis settings
    REDIS_HOST = os.environ.get('OPENSHIFT_REDIS_HOST')
    REDIS_PORT = os.environ.get('OPENSHIFT_REDIS_PORT')
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')


# Cache settings

CACHES = {
    "default": {
        "BACKEND": "redis_cache.cache.RedisCache",
        "LOCATION": '%s:%s:%d' % (REDIS_HOST, REDIS_PORT, REDIS_DB),
        'TIMEOUT': 60,
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
            'SOCKET_TIMEOUT': 5,
            'PASSWORD': REDIS_PASSWORD,
        }
    }
}

# Static files (CSS, JavaScript, Images)
# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "../static"),
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)

STATIC_URL = '/static/'

INSTAGRAM_ID = '0e5e6d62e1f94f72a40180c9cd5bdbe0'