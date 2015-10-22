'''This module sets the configuration for a local development

'''
from .common import *

import os

DEBUG = False
TEMPLATE_DEBUG = False

STATIC_ROOT = '/home/{{ cookiecutter.remote_user }}/sites/{{ cookiecutter.repo_name }}/shared/static/'
MEDIA_ROOT = '/home/{{ cookiecutter.remote_user }}/sites/{{ cookiecutter.repo_name }}/media/'
# CKEDITOR
CKEDITOR_CONFIGS['default']['contentsCss'] = [
    STATIC_URL + '{{ cookiecutter.repo_name }}/css/vendor.min.css',
    STATIC_URL + '{{ cookiecutter.repo_name }}/css/abidibo-net.min.css',
    STATIC_URL + '{{ cookiecutter.repo_name }}/src/css/ckeditor.css']
