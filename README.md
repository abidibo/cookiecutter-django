# Cookiecutter template for django projects

This is just another cookiecutter template for django projects, matching my job requirements.
There are many out there which are great but I needed one following my consolidated workflow.

Running this you will have a development ready django project with all the packages installed and the database created and ready to go.

You will be provided with a bin command which will set up the remote machine for you, using ansible. 

## Environment

### Local

- mysql db
- django development server

### Remote

- mysql db
- nginx server
- uwsgi

## Features

- django db settings managed with environment variables
- some must-have (in my opinion) packages installed
- flatpatges with integrated ckeditor
- git repository initialized and ready
- fabfile ready for deployment
- bootstrap-4-dev
- bin command to set up your production machine

## Constraints

- mysql everywhere and already installed in the __local__ machine
- environment variables for configuration

## Python Packages

- Django==1.8.5
- django-getenv==1.3.1
- MySQL-python==1.2.5
- Fabric==1.10.2
- Pillow==3.0.0
- django-ckeditor==5.0.2
- django-cleanup==0.4.0
- django-pipeline==1.5.4
- django-simple-captcha==0.4.6
- django-tagging==0.4
- sorl-thumbnail==12.3
- ansible==1.9.4
- python-dotenv==0.1.5

###Optional:

- django-disqus==0.5
- django-filer==0.9.12
- django-grappelli==2.7.1
- django-suit==0.2.15

### Local dev

- django-debug-toolbar==1.4

### Production

- uWSGI==2.0.11.2

## Frontend

### Vendor

- jQuery 1.11.3
- moment.js
- bootstrap v4.0.0-alpha
- FontAwesome

## Getting started

Install cookieclutter

`$ pip install cookieclutter`

Run cookieclutter against this repo

`$ cookiecutter https://github.com/abidibo/cookiecutter-django`

Answer the following questions:

- __project_name__: name of the project. Default "My New Project"
- __project_description__: project description. Default "My New Project description"
- __repo_name__: name of the repository. Default "[project_name | lower | replace(' ', '-')]"
- __admin__: django admin app package. Possible values: django-suit, django-grappelli, default. Default "default"
- __use_filer__: whether or not to install django-filer [y|n]. Default "n"
- __use_disqus__: whether or not to install django-disqus [y|n]. Default "n"
- __language_code__: language code. Default "en-us"
- __timezone__: timezone. Default "Europe/Rome"
- __author__: project author. Default "abidibo"
- __email__: project author email. Default "abidibo@gmail.com"
- __remote\_user__: user for deployment to the production server. Default "[repo_name]"
- __domain__: production domain. Default "www.example.com"
- __remote\_root\_mysql\_pwd__: password for the remote mysql root user. Default "". You can set it later inside the `provisioning/playbooks/roles/database/templates/.my.cnf` file
- __db\_user__: user for the remote database. Default "[remote\_user]"
- __db\_password__: user password for the remote database. Default ""

Then provide your sudo password in order to provision your local environment.

If all works great now you should have:

- a new folder (I'll call it root) containing all your bootstrapped project
- all the necessary packages installed
- a fresh virtualenv with all the dependencies already installed (folder `.virtualenv` in the root)
- a new database ready to go with, all migrations applied
- a new git repository initialized
- a README file explaining how to proceed

Now:

    $ cd [repo_name]
    $ python [repo_name]/manage.py createsuperuser
    $ bin/runserver

And visit http://localhost:8000

## Notes

- change the SECRET_KEY setting in your `[repo_name]/settings/common.py` settings file.
- you can also not specify the remote params during the installation. You will have a working local environment ready to go. But in this case you'll have to set them manually to configure the remote setup script which uses ansible. In this case check the followinf files:
    - `provisioning/ansible_remote_inventory`
    - `provisioning/ansible_remote_variables`

## Remote setup

Remote setup is done with ansible, using the root user. Run

    $ bin/ansible_remote

and provide the root password when prompted.

If all goes well now you should have your remote machine ready for deploy.
Visit your domain and you should see a maintenance page already there.

### Troubleshooting

#### SSH connection error
If you see this error

    fatal: [remote] => Using a SSH password instead of a key is not possible because Host Key checking is enabled and sshpass does not support this.  Please add this host's fingerprint to your known_hosts file to manage this host.

means you missed adding an entry for one or more hosts in the ~/.ssh/known_hosts file, it's enough to 

#### DB task error
If an error occurs in the create db user task:

    msg: (1396, "Operation CREATE USER failed for ...

maybe you're trying to create a user which already existed and was delete. In this case just run this sql in the mysql database:

    FLUSH PRIVILEGES;

see [this answer on stack overflow](http://stackoverflow.com/questions/5555328/error-1396-hy000-operation-create-user-failed-for-jacklocalhost])
