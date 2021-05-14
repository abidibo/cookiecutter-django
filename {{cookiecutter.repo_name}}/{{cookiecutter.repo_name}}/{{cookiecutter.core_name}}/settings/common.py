from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import ugettext_lazy as _

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = getenv('SECRET_KEY')

ADMINS = (
    ('{{ cookiecutter.author }}', '{{ cookiecutter.email }}'),
)

AUTH_USER_MODEL = 'core.User'

SITE_ID = 1

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('DB_NAME'),
    }
}

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

INSTALLED_APPS = (
    '{{ cookiecutter.core_name }}',
    {% if cookiecutter.use_django_baton == 'y' %}
    'baton',
    {% endif %}
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django_extensions',
    'django_cleanup',
    'pages',
    'constance.backends.database',
    'lineup.apps.LineupConfig',
    'taggit',
    'subject_imagefield',
    'sorl.thumbnail',
    'pipeline',
    'ckeditor',
    'ckeditor_uploader',
    {% if cookiecutter.use_user_agents == 'y' %}
    'django_user_agents',
    {% endif %}
    {% if cookiecutter.use_filer == 'y' %}
    'easy_thumbnails'
    'filer',
    {% endif %}
    'mptt',
    {% if cookiecutter.use_simple_captcha == 'y' %}
    'captcha',
    {% endif %}
    'apps.SettingsConfig',
    {% if cookiecutter.use_django_baton == 'y' %}
    'baton.autodiscover',
    {% endif %}
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pages.middleware.PageFallbackMiddleware',
    {% if cookiecutter.use_user_agents == 'y' %}
    'django_user_agents.middleware.UserAgentMiddleware',
    {% endif %}
)

ROOT_URLCONF = '{{ cookiecutter.core_name }}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'constance.context_processors.config',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                '{{ cookiecutter.core_name }}.context_processors.debug',
                '{{ cookiecutter.core_name }}.context_processors.absurl',
            ],
            'libraries': {
                'sorl_thumbnail': 'sorl.thumbnail.templatetags.thumbnail',
            },
        },
    },
]

WSGI_APPLICATION = '{{ cookiecutter.core_name }}.wsgi.application'

# Internationalization

LANGUAGE_CODE = '{{ cookiecutter.language_code }}'

TIME_ZONE = '{{ cookiecutter.timezone }}'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Constance

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'HIDE_ARCHIVED': (True, _('Hide from admin lists archived records')),
    'SITE_TITLE': ('{{ cookiecutter.project_name }}', _('Site title')),
    'META_TITLE': ('{{ cookiecutter.project_name }}', _('Meta title')),
    'META_DESCRIPTION': ('{{ cookiecutter.project_description }}', _('Meta description')),
    'META_KEYWORDS': ('', _('Meta keywords')),
    'ROBOTS': ('User-agent: *\nDisallow:', _('Contents of robots.txt file')),
    'OG_TITLE': ('{{ cookiecutter.project_name }}', _('Open Graph title')),
    'OG_TYPE': ('website', _('Open Graph type')),
    'OG_DESCRIPTION': ('{{ cookiecutter.project_description }}', _('Open Graph description')),
    'OG_IMAGE': ('', _('Open Graph image')),
    'TWITTER_TITLE': ('{{ cookiecutter.project_name }}', _('Twitter title')),
    'TWITTER_DESCRIPTION': ('{{ cookiecutter.project_description }}', _('Twitter description')),
    'TWITTER_CREATOR': ('', _('Twitter creator')),
    'TWITTER_IMAGE': ('', _('Twitter image')),
}

CONSTANCE_CONFIG_FIELDSETS = {
    'SEO': ('SITE_TITLE', 'META_TITLE', 'META_DESCRIPTION', 'META_KEYWORDS', 'ROBOTS', ),
    'Facebook Sharing': ('OG_TITLE', 'OG_TYPE', 'OG_DESCRIPTION',
                            'OG_IMAGE', ),
    'Twitter Sharing': ('TWITTER_TITLE', 'TWITTER_DESCRIPTION',
                           'TWITTER_CREATOR', 'TWITTER_IMAGE', ),
    'Administration': ('HIDE_ARCHIVED', ),
}

# Static files (CSS, JavaScript, Images)

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)
STATIC_URL = '/static/'

# Uploaded files

MEDIA_URL = '/media/'
FILE_UPLOAD_PERMISSIONS = 0o644

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

{% if cookiecutter.use_django_baton == 'y' %}
# Admin

BATON = {
    'SITE_HEADER': '{{ cookiecutter.project_name }}',
    'SITE_TITLE': '{{ cookiecutter.project_name }}',
    'INDEX_TITLE': 'Site administration',
    'MENU': (
        {'type': 'title', 'label': 'System',  'apps': ('auth', 'sites', 'constance', )},
        {'type': 'model', 'app': 'core', 'name': 'user', 'label': 'Users', 'icon':'fa fa-user'},
        {'type': 'model', 'app': 'auth', 'name': 'group', 'label': 'Groups', 'icon':'fa fa-users'},
        {'type': 'model', 'app': 'sites', 'name': 'site', 'label': 'Sites', 'icon':'fa fa-leaf'},
        {'type': 'model', 'app': 'constance', 'name': 'config', 'label': 'Settings', 'icon':'fa fa-cogs'},

        {% if cookiecutter.use_filer == 'y' %}
        {'type': 'title', 'label': 'Resources',  'apps': ('filer', )},
        {'type': 'app', 'name': 'filer', 'label': 'File manager', 'icon':'fa fa-file'},
        {% endif %}

        {'type': 'title', 'label': 'Navigation',  'apps': ('treenav', )},
        {'type': 'model', 'app': 'treenav', 'name': 'menuitem', 'label': 'Menu', 'icon':'fa fa-bars'},

        {'type': 'title', 'label': 'Contents',  'apps': ('pages', )},
        {'type': 'model', 'app': 'pages', 'name': 'page', 'label': 'Pages', 'icon':'fa fa-book'},
    ),
    'COPYRIGHT': '© {% now 'utc', '%Y' %} {{ cookiecutter.domain }}',
    'SUPPORT_HREF': 'mailto:stefano.contini@otto.to.it',
    'POWERED_BY': '<a href="https://www.abidibo.net">abidibo</a>'
}
{% endif %}

# Taggit

TAGGIT_CASE_INSENSITIVE = True

# Ckeditor

CKEDITOR_UPLOAD_PATH = 'ckeditor/'
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

# Pipeline

PIPELINE = {
    'STYLESHEETS': {
        'vendor': {
            'source_filenames': (
                '{{ cookiecutter.core_name }}/src/vendor/Font-Awesome/scss/font-awesome.scss', # noqa
                '{{ cookiecutter.core_name }}/app/node_modules/bootstrap/dist/css/bootstrap.min.css' # noqa
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
                '{{ cookiecutter.core_name }}/app/node_modules/bootstrap/dist/js/bootstrap.bundle.min.js', # noqa
            ),
            'output_filename': '{{ cookiecutter.core_name }}/js/vendor.min.js'
        },
        '{{ cookiecutter.repo_name }}': {
            'source_filenames': (
                '{{ cookiecutter.core_name }}/app/src/js/{{ cookiecutter.core_name }}.js', # noqa
            ),
            'output_filename': '{{ cookiecutter.core_name }}/js/{{ cookiecutter.core_name }}.min.js' # noqa
        },
    },
    'COMPILERS': ('pipeline.compilers.sass.SASSCompiler', ),
    'CSS_COMPRESSOR': None,
    'JS_COMPRESSOR': None,
    'MIMETYPES': (
      ('text/coffeescript', '.coffee'),
      ('text/less', '.less'),
      ('text/javascript', '.js'),
      ('text/x-sass', '.sass'),
      ('text/x-scss', '.scss')
    )
}

{% if cookiecutter.use_filer == 'y' %}
# Filer

THUMBNAIL_HIGH_RESOLUTION = True
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)
{% endif %}

# Logging

LOG_LEVEL = getenv('LOG_LEVEL', 'INFO')

LOGGING_DEFAULT = {
    'handlers': ['console', 'file'],
    'level': LOG_LEVEL,
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
            'level': LOG_LEVEL,
            'class':'logging.NullHandler',
        },
        'console':{
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        # configure the log to be rotated daily
        'file': {
            'level': LOG_LEVEL,
            'formatter': 'verbose',
            'class': 'logging.handlers.TimedRotatingFileHandler',
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
            'level': LOG_LEVEL,
            'propagate': True,
        },
       'django.template': {
            'handlers': ['file'],
            'level': 'INFO',
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
            'level': LOG_LEVEL,
        },
        '{{ cookiecutter.core_name }}': LOGGING_DEFAULT,
        '': LOGGING_DEFAULT,
    },
}
