# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Getting Started

- clone the repository    
  `$ git clone https://github.com/{{ cookiecutter.author }}/{{ cookiecutter.repo_name }}.git`
- cd the new project    
  `$ cd [repo_name]`
- create a virtualenv    
  `$ virtualenv --no-site-packages .virtualenv`
- activate it    
  `$ source .virtualenv/bin/activate`
- install requirements    
  `$ pip install -r [repo_name]/requirements/local.txt`
- create a .env file    
  `$ touch .env`
- config environment    
  `$ dotenv set DJANGO_SETTINGS_MODULE {{ cookiecutter.core_name }}.settings.local`    
  `$ dotenv set DB_PASSWORD <whatever>`
  `$ dotenv set SECRET_KEY <whatever>`
- run the server    
  `$ bin/runserver`
- enjoy    
  `http://localhost:8000`

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


## Deploy and Stuff

In the deployment process, the last revision of the git repository is deployed to the remote server.
So be sure to have committed all your changes:

    $ git add --all
    $ git commit -a -m "first commit"

Be sure the provided remote user has ssh access to the remote host, then deploy should be as easy as:

    $ cd [repo_name]
    $ fab production deploy

launched inside the root/repo\_name folder. This command does the following things:

- create an archive of the last repository revision
- upload it to the server
- untar it in a folder "app-revision\_id" inside the releases folder
- copy the .env file inside this folder
- upgrade the virtualenv
- collectstatic
- migrations
- move the current release in the previous release (releases/previous)
- link the releases/current folder to the new release folder
- restart uwsgi and nginx
- open a shell in the remote

When performing the first deploy you can create a superuser account using the shell which the script leaves open at the end.

###Other useful fab commands

#### rollback

    $ fab production rollback

If the deploy revision is broken, or introduces unexpected errors, with this command
it is possible to rollback to the previous revision. Launching it another time will swap between the two revisions.

#### restart\_uwsgi

    $ fab production restart_uwsgi

Restarts the uwsgi service

#### restart\_server

    $ fab production restart_server

Restarts the web server

#### restart

    $ fab production restart

Restarts the uwsgi service and the web server

#### dump\_db\_snapshot

    $ fab production dump_db_snapshot

Downloads the production current db snapshot in the backup folders. The dumped file has the remote current revision name.

Requires the remote db user password.

#### load\_db\_snapshot

    $ fab production load_db_snapshot

Loads the current remote db snapshot in the local db.

Requires the remote db user password.
