# Cookiecutter template for django projects

This is just another cookiecutter template for django projects, matching my job requirements.
There are many out there which are great but I needed one following my consolidated workflow.

Running this you will have:

- a development ready django project with all the packages installed and the database created and ready to go.
- a bin command which will set up the remote machine for you (using ansible) and will display a maintenance page
- some production commands to manage the deploy and related stuff.


> **Important**    
> For the bootstrap4 version, please use the bootstrap branch, the master one uses semantic-ui.


## Environment

[Cookiecutter](https://github.com/audreyr/cookiecutter) is uset to create a working directory already configured.

[Ansible](https://github.com/ansible/ansible) is used to set up the local and remote machines

[Fabric](http://www.fabfile.org/) is used to manage the deploy and other related tasks.

### Local

- mysql db
- django development server

### Remote

- mysql db
- nginx server
- uwsgi

## Features

- django db settings managed with environment variables
- some must-have (in my opinion) packages installed:
    - [django-pipeline](https://github.com/cyberdelia/django-pipeline)
    - [django-ckeditor](https://github.com/django-ckeditor/django-ckeditor)
    - [django-treenav](https://github.com/caktus/django-treenav)
    - [django-cleanup](https://github.com/un1t/django-cleanup)
    - [django-constance](https://github.com/jazzband/django-constance)
    - [django-user_agents](https://github.com/selwin/django-user_agents)
    - [django-extensions](https://github.com/django-extensions/django-extensions)
    - [django-simple-captcha](https://github.com/mbi/django-simple-captcha)
    - [django-subject-imagefield](https://github.com/otto-torino/django-subject-imagefield)
    - [django-taggit](https://github.com/alex/django-taggit)
    - [easy-thumbnails](https://github.com/SmileyChris/easy-thumbnails)
    - [django-debug-toolbar](https://github.com/django-debug-toolbar/django-debug-toolbar)
    - [django-baton](https://github.com/otto-torino/django-baton) (optional)
    - [django-suit](http://djangosuit.com/) (optional)
    - [django-grappelli](https://github.com/sehmaschine/django-grappelli) (optional)
    - [django-filer](https://github.com/stefanfoulis/django-filer) (optional)
    - [django-disqus](https://github.com/arthurk/django-disqus) (optional)
- pages with integrated ckeditor
- git repository initialized and ready
- bootstrap 4.2.1
- bin command to set up your production machine
- fabfile ready for deployment

## Constraints

- environment variables for configuration

## Frontend

### Vendor

jQuery as js framework, bootstrap as css framework, momentjs to deal with datetime objects.

- jQuery 1.11.3
- moment.js
- bootstrap v4.2.1
- FontAwesome 4.7.0

## Getting started

Install cookiecutter

`$ pip install cookiecutter`

Install ansible (and run it under python3)

`pip3 install ansible`

Run cookiecutter against this repo

`$ cookiecutter https://github.com/abidibo/cookiecutter-django`

Answer the following questions:

- __project_name__: name of the project. Default "My New Project"
- __project_description__: project description. Default "My New Project description"
- __repo\_name__: name of the repository. Default "[project\_name | lower | replace(' ', '-')]"
- __core\_name__: name of the main application. Default "[repo\_name | replace('-', '\_')]"
- __admin__: django admin app package. Possible values: django-baton, django-suit, django-grappelli, default. Default "django-baton"
- __use_filer__: whether or not to install django-filer [y|n]. Default "n"
- __use_disqus__: whether or not to install django-disqus [y|n]. Default "n"
- __language_code__: language code. Default "en-us"
- __timezone__: timezone. Default "Europe/Rome"
- __author__: project author. Default "abidibo"
- __email__: project author email. Default "abidibo@gmail.com"
- __remote\_user__: user for deployment to the production server. Default "[repo\_name]"
- __domain__: production domain. Default "www.example.com"
- __remote\_root\_mysql\_pwd__: password for the remote mysql root user. Default "". You can set it later inside the `provisioning/playbooks/roles/database/templates/.my.cnf` file
- __db\_user__: user for the remote database. Default "[remote\_user]"
- __db\_user_pwd__: user password for the remote database. Default ""
- __webapp\_dir__: absolute path to the remote deploy directory

__Then provide your sudo password in order to provision your local environment.__

If all works great now you should have:

- a new folder (I'll call it root) containing all your bootstrapped project
- all the necessary packages installed
- a fresh virtualenv with all the dependencies already installed (folder `.virtualenv` in the root)
- a new database ready to go with, all migrations applied
- a new git repository initialized
- a README file explaining how to clone and get started with the project

Now:

    $ cd [repo_name]
    $ python [repo_name]/manage.py createsuperuser
    $ bin/runserver

And visit http://localhost:8000

### Notes

- setup local environment manually    
  maybe you don't want ansible to setup the local environment for you (for example if you are on a mac some commands will fail), so just
  interrupt the execution of cookiecutter (CTRL-C) when you're prompted for the sudo password. You can then check the provisioning files,
  change them and then launch `bin/ansible_local` manually


- change the SECRET_KEY:

    `$ dotenv set SECRET_KEY <secret_key_here>`

  you can change the remote SECRET KEY adding a line

    `SECRET_KEY='<value here>'`

- you can also not specify the remote params during the installation. You will have a working local environment ready to go. But in this case you'll have to set them manually to configure the remote setup script which uses ansible. In this case check the followinf files:
    - `provisioning/ansible_remote_inventory`
    - `provisioning/ansible_remote_variables`
    - `[repo_name]/fabfile.py`

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

means you missed adding an entry for one or more hosts in the ~/.ssh/known_hosts file, it's enough to try an ssh connection in order to add the domain to your list, then relauch `bin/ansible_remote`

#### DB task error
If an error occurs in the create db user task:

    msg: (1396, "Operation CREATE USER failed for ...

maybe you're trying to create a user which already existed and was delete. In this case just run this sql in the mysql database:

    FLUSH PRIVILEGES;

see [this answer on stack overflow](http://stackoverflow.com/questions/5555328/error-1396-hy000-operation-create-user-failed-for-jacklocalhost])

## Deploy and Stuff

In the deployment process, the last revision of the git repository is deployed to the remote server.
So be sure to have committed all your changes:

    $ git add --all
    $ git commit -a -m "first commit"

Be sure the provided remote user has ssh access to the remote host, then deploy should be as easy as:

    $ cd [repo_name]
    $ fab production deploy

launched inside the `root/repo_name` folder. This command does the following things:

- create an archive of the last repository revision
- upload it to the server
- untar it in a folder "`app-revision_id`" inside the releases folder
- copy the .env file inside this folder
- upgrade the virtualenv
- collectstatic
- migrations
- move the current release in the previous release (releases/previous)
- link the releases/current folder to the new release folder
- restart uwsgi and reload nginx
- open a shell in the remote

When performing the first deploy you can create a superuser account using the shell which the script leaves open at the end.

###Other useful fab commands

#### rollback

    $ fab production rollback

If the deploy revision is broken, or introduces unexpected errors, with this command
it is possible to rollback to the previous revision. Launching it another time will swap between the two revisions.

#### reloadServer

    $ fab production reloadServer

Reloads the web server

#### restart

    $ fab production restart

Restarts the uwsgi service and the web server

#### dumpDbSnapshot

    $ fab production dumpDbSnapshot

Downloads the production current db snapshot in the backup folders. The dumped file has the remote current revision name.

#### loadDbSnapshot

    $ fab production loadDbSnapshot

Loads the current remote db snapshot in the local db.

#### offline

    $ fab production offline

Puts the site in maintenance mode

#### online

    $ fab production online

Exits from maintenance mode

#### getRemoteRevision

    $ fab production getRemoteRevision

Prints to screen the currently deployed revision
