from .common import *

DEBUG = False

STATIC_ROOT = '{{ cookiecutter.webapp_dir }}/static/'
MEDIA_ROOT = '{{ cookiecutter.webapp_dir }}/media'
LOGGING['handlers']['file']['filename'] = '{{ cookiecutter.webapp_dir }}/logs/application.log'

# Ckeditor

CKEDITOR_CONFIGS['default']['contentsCss'] = [
    STATIC_URL + '{{ cookiecutter.core_name }}/css/vendor.min.css',
    STATIC_URL + '{{ cookiecutter.core_name }}/css/{{ cookiecutter.core_name }}.min.css',
    STATIC_URL + '{{ cookiecutter.core_name }}/src/css/ckeditor.css']

# Database

DATABASES['default'] |= {
    'USER': getenv('DB_USER'),
    'PASSWORD': getenv('DB_PASSWORD'),
}
