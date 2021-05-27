#!/usr/bin/env python3

##
# Does the following:
#
# 1 - Enables gitignore
# 2 - Installs system required packages
# 3 - Creates a new database
# 4 - Creates a virtualenv
# 5 - Installs app requirements
# 6 - Db initial migration
# 7 - Repository initialization
# 8 - Installs sass gem
# 9 - Activates the created virtualenv
##

from shutil import move, rmtree
from subprocess import run
from collections import OrderedDict

context = {{ cookiecutter }}

print('\n' + 'POST HOOK' + '\n')

if context['use_django_baton'] == 'n':
    print('Remove unused baton and constance admin template' + '\n')
    rmtree('./{{ cookiecutter.repo_name }}/{{ cookiecutter.core_name }}/templates/admin')

print('Enable gitignore')
move('gitignore', '.gitignore')

print('Launch saltstack')
run(['sh', 'local.sh'], cwd='provisioning')

# print('Create python virtual enironment')
# run(['pyenv', 'virtualenv', '{{cookiecutter.python_version}}' '{{cookiecutter.repo_name|replace('-', '')}}'])
# run(['pyenv', 'local', '{{cookiecutter.repo_name|replace('-', '')}}'])
