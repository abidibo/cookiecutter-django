#!/usr/bin/env python

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

import os
import shutil
import collections

context = {{ cookiecutter }}

if context['admin'] != 'django-baton':
    print('\n')
    print('POST HOOK' + '\n')
    print('removing unused baton and constance admin template' + '\n')
    shutil.rmtree('./{{ cookiecutter.repo_name }}/{{ cookiecutter.core_name }}/templates/admin')

shutil.move('gitignore', '.gitignore')
os.system('./bin/ansible_local')
os.system('source ./.virtualenv/bin/activate')
