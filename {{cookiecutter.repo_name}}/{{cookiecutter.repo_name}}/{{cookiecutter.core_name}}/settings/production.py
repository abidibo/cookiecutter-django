'''This module sets the configuration for a local development

'''
from .common import *

import os

DEBUG = False

ALLOWED_HOSTS = ['{{ cookiecutter.domain }}',]

STATIC_ROOT = '{{ cookiecutter.webapp_dir }}/static/'
MEDIA_ROOT = '{{ cookiecutter.webapp_dir }}/media'
# CKEDITOR
CKEDITOR_CONFIGS['default']['contentsCss'] = [
    STATIC_URL + '{{ cookiecutter.core_name }}/css/vendor.min.css',
    STATIC_URL + '{{ cookiecutter.core_name }}/css/{{ cookiecutter.core_name }}.min.css',
    STATIC_URL + '{{ cookiecutter.core_name }}/src/css/ckeditor.css']
 
LOGGING['handlers']['file']['filename'] = here('..', '..', '..', '..', os.path.join('logs', 'debug.log'))
