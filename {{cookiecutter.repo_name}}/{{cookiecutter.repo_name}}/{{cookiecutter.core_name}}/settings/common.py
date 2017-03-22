"""
Django settings for {{ cookiecutter.project_name }} project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from dotenv import load_dotenv
from getenv import env

here = lambda *x: os.path.join(os.path.dirname( # noqa
                               os.path.realpath(__file__)), *x)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # noqa

dotenv_path = here('..', '..', '.env')
load_dotenv(dotenv_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', '49saa%ruey1&!nveiz*f(cu$)0pje8wz7u++y-0ljd2)9r)j8h') # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

ADMINS = (
    ('{{ cookiecutter.author }}', '{{ cookiecutter.email }}'),
)

# SITE
SITE_ID = 1

# MAIL
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME', 'db{{ cookiecutter.repo_name }}'),
        'HOST': env('DB_HOST', 'localhost'),
        'USER': env('DB_USER', '{{ cookiecutter.repo_name }}'),
        'PASSWORD': env('DB_PASSWORD', required=True),
        'PORT': '',
        'OPTIONS': {
            'init_command': 'SET default_storage_engine=InnoDB',
        }
    }
}

# Application definition

INSTALLED_APPS = (
    '{{ cookiecutter.core_name }}',
    {% if cookiecutter.admin == 'django-suit' %}'suit',{% elif cookiecutter.admin == 'django-grappelli' %}'grappelli',{% endif %}
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'ckeditor',
    'ckeditor_uploader',
    'pipeline',
    {% if cookiecutter.use_filer == 'y' %}
    'filer',
    'mptt',
    {% endif %}
    'django_cleanup',
    'captcha',
    'easy_thumbnails',
    {% if cookiecutter.use_disqus == 'y' %}'disqus',{% endif %}
    'taggit',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = '{{ cookiecutter.core_name }}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': False,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.debug',
            ],
        },
    },
]

WSGI_APPLICATION = '{{ cookiecutter.core_name }}.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = '{{ cookiecutter.language_code }}'

TIME_ZONE = '{{ cookiecutter.timezone }}'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Uploaded files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ADMIN
{% if cookiecutter.admin == 'django-grappelli' %}
GRAPPELLI_ADMIN_TITLE = '{{ cookiecutter.project_name }} - Amministrazione'
{% elif cookiecutter.admin == 'django-suit' %}
SUIT_CONFIG = {
    'ADMIN_NAME': '{{ cookiecutter.project_name }}',
    'MENU': (

        '-',

        {'app': 'auth', 'label': 'Authentication', 'icon':'icon-lock'},
        {'app': 'sites', 'label': 'Sites', 'icon':'icon-leaf'},

        {% if cookiecutter.use_filer == 'y' %}
        '-',

        {'app': 'filer', 'label': 'Files', 'icon':'icon-file'},

        {% endif %}
        '-',

        {'app': 'flatpages', 'label': 'Pages', 'icon':'icon-book'},

    )
}
{% endif %}

# TAGGIT
TAGGIT_CASE_INSENSITIVE = True

# CKEDITOR
CKEDITOR_UPLOAD_PATH = 'ckeditor/'
CKEDITOR_JQUERY_URL = ''
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'toolbar_Basic': [
                ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_Full': [
                ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker', 'Undo', 'Redo'], # noqa
                ['NumberedList','BulletedList'],
                ['Link','Unlink','Anchor'],
                '/',
                ['Image', 'Flash', 'Table', 'HorizontalRule'],
                ['TextColor', 'BGColor'],
                ['SpecialChar'], ['PasteFromWord', 'PasteText'], ['Source']
        ],
        'toolbar': 'Full',
        'resize_dir': 'both',
        'resize_minWidth': 300,
        'height': 291,
        'width': '100%',
        'filebrowserWindowWidth': 940,
        'filebrowserWindowHeight': 725,
        'removePlugins': 'stylesheetparser',
        'allowedContent': True,
        'extraAllowedContent': 'iframe[*]',
        'stylesSet': 'core_styles:/static/{{ cookiecutter.core_name }}/src/js/ckeditor_styles.js',
    }
}

# pipeline
PIPELINE = {
    'STYLESHEETS': {
        'vendor': {
            'source_filenames': (
                '{{ cookiecutter.core_name }}/src/vendor/tether/css/tether.min.css', # noqa
                '{{ cookiecutter.core_name }}/src/vendor/Font-Awesome/scss/font-awesome.scss', # noqa
            ),
            'output_filename': '{{ cookiecutter.core_name }}/css/vendor.min.css', # noqa
        },
        '{{ cookiecutter.repo_name }}': { # bootstrap + custom
            'source_filenames': (
                '{{ cookiecutter.core_name }}/src/scss/styles.scss',
            ),
            'output_filename': '{{ cookiecutter.core_name }}/css/{{ cookiecutter.core_name }}.min.css', # noqa
        },
    },
    'JAVASCRIPT': {
        'vendor': {
            'source_filenames': (
                '{{ cookiecutter.core_name }}/src/vendor/tether/js/tether.min.js', # noqa
                '{{ cookiecutter.core_name }}/src/vendor/bootstrap/js/bootstrap.min.js', # noqa
                '{{ cookiecutter.core_name }}/src/vendor/moment/moment-with-locales.min.js', # noqa
            ),
            'output_filename': '{{ cookiecutter.core_name }}/js/vendor.min.js'
        },
        '{{ cookiecutter.repo_name }}': {
            'source_filenames': (
                '{{ cookiecutter.core_name }}/src/js/{{ cookiecutter.core_name }}.js', # noqa
            ),
            'output_filename': '{{ cookiecutter.core_name }}/js/{{ cookiecutter.core_name }}.min.js' # noqa
        },
    },
    'COMPILERS': ('pipeline.compilers.sass.SASSCompiler', ),
    'CSS_COMPRESSOR': None,
    'JS_COMPRESSOR': None,
}

{% if cookiecutter.use_disqus == 'y' %}
DISQUS_API_KEY = ''
DISQUS_WEBSITE_SHORTNAME = ''
{% endif %}

{% if cookiecutter.use_filer == 'y' %}
THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)
{% endif %}

# LOGGING

LOGGING_DEFAULT = {
    'handlers': ['console', 'file'],
    'level': 'DEBUG',
    'propagate': True,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s' # noqa
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
       'null': {
            'level': 'DEBUG',
            'class':'logging.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        # configure the log to be rotated daily
        # see https://docs.python.org/2.7/library/logging.handlers.html#logging.handlers.TimedRotatingFileHandler
        'file': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': here('..', '..', '..', os.path.join('logs', 'debug.log')), # noqa
            'when':     'midnight',
        },

        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins', 'console', 'file',],
            'level': 'ERROR',
            'propagate': False,
        },
        # http://stackoverflow.com/questions/7768027/turn-off-sql-logging-while-keeping-settings-debug
       'django.db.backends': {
            'handlers': ['null'],  # Quiet by default!
            'propagate': False,
            'level':'DEBUG',
        },
        '{{ cookiecutter.core_name }}': LOGGING_DEFAULT,
        '':                             LOGGING_DEFAULT,# root logger
    },
}
