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

from os import system
from shutil import move, rmtree
from collections import OrderedDict

context = {{ cookiecutter }}

if context['use_django_baton'] == 'n':
    print('\n')
    print('POST HOOK' + '\n')
    print('removing unused baton and constance admin template' + '\n')
    rmtree('./{{ cookiecutter.repo_name }}/{{ cookiecutter.core_name }}/templates/admin')

move('gitignore', '.gitignore')
#system('./bin/ansible_local')
