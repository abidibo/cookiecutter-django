#!/bin/bash

##
# Does the following:
#
# 1 - Installs system required packages
# 2 - Creates a new database
# 3 - Creates a virtualenv
# 4 - Installs app requirements
# 5 - Db initial migration
# 6 - Repository initialization
# 7 - Installs sass gem
# 8 - Activates the created virtualenv
##

bin/ansible_local
source .virtualenv/bin/activate
