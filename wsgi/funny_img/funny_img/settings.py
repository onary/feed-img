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
    # 'taggit',

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
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

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

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''
STATIC_ROOT = ''

if OPENSHIFT:
    MEDIA_ROOT = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR'), 'wsgi', 'media')
    STATIC_ROOT = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR'), 'wsgi', 'static')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "../static"),
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
)

STATIC_URL = '/static/'
