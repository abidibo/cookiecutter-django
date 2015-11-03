'''This module sets the configuration for a local development

'''
from .common import *

import os

DEBUG = True

INSTALLED_APPS += (
    'debug_toolbar',
)

# MAIL
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CKEDITOR
CKEDITOR_CONFIGS['default']['contentsCss'] = [
    STATIC_URL + '{{ cookiecutter.core_name }}/src/vendor/Font-Awesome/scss/font-awesome.css',
    STATIC_URL + '{{ cookiecutter.core_name }}/src/scss/styles.css',
    STATIC_URL + '{{ cookiecutter.core_name }}/src/css/ckeditor.css']

# DEBUG_TOOLBAR
JQUERY_URL = ''
