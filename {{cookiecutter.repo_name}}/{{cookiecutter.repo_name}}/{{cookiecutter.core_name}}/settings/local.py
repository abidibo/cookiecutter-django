from .common import *

DEBUG = True

ALLOWED_HOSTS = []

STATIC_ROOT = BASE_DIR / 'static'
MEDIA_ROOT = BASE_DIR / 'media'
LOGGING['handlers']['file']['filename'] = BASE_DIR / 'logs' / '..' / 'application.log'

INTERNAL_IPS = ('127.0.0.1', )  # debug toolbar

INSTALLED_APPS += (
    'debug_toolbar',
)

MIDDLEWARE = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
) + MIDDLEWARE

TEMPLATES[0]['OPTIONS']['debug'] = True

# Mail

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Ckeditor

CKEDITOR_CONFIGS['default']['contentsCss'] = [
    STATIC_URL + '{{ cookiecutter.core_name }}/src/vendor/Font-Awesome/scss/font-awesome.css',
    STATIC_URL + '{{ cookiecutter.core_name }}/src/scss/styles.css',
    STATIC_URL + '{{ cookiecutter.core_name }}/src/css/ckeditor.css']
