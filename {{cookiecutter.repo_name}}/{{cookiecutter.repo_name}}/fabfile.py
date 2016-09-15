import os
from contextlib import contextmanager as _contextmanager

from fabric.api import task
from fabric.state import env
from fabric.context_managers import show, settings, cd, prefix
from fabric.contrib.files import is_link
from fabric.operations import run, sudo, get, local, put, open_shell
from fabric.contrib import files

# path from here
here = lambda *x: os.path.join(os.path.dirname(
                               os.path.realpath(__file__)), *x)

# https://gist.github.com/lost-theory/1831706
class CommandFailed(Exception):
    def __init__(self, message, result):
        Exception.__init__(self, message)
        self.result = result

def erun(*args, **kwargs):
    with settings(warn_only=True):
        result = run(*args, **kwargs)
    if result.failed:
        raise CommandFailed("args: %r, kwargs: %r, error code: %r" % (args, kwargs, result.return_code), result)
    return result

@_contextmanager
def remote_virtualenv(path):
    # use when need to execute commands with activated virtualenv
    with cd(path):
        with prefix('source %(path)s/.virtualenv/bin/activate' % env):
            yield

@task
def production():
    """Production server settings"""
    env.settings = 'production'
    env.user = '{{ cookiecutter.remote_user }}'
    env.path = '{{ cookiecutter.webapp_dir }}'
    env.hosts = ['{{ cookiecutter.domain }}']

@task
def get_remote_revision():
    """ Returns and prints the current deployed remote revision """
    current_app_dir = erun('basename $(readlink -f %(path)s/releases/current)' % env)
    try:
        _, remote_revision = current_app_dir.split('-')
    except Exception as e:
        print e
        remote_revision = 'unknown'

    print remote_revision
    return remote_revision

def describe_revision(head='HEAD'):
    """ Describes the current local revision"""
    actual_tag = local('git describe --always %s' % head, capture=True)
    return actual_tag

def get_release_filename():
    return '%s.tar.gz' % describe_revision()

def get_release_filepath():
    releases_dir = here('..', 'releases')
    if not os.path.exists(releases_dir):
        os.makedirs(releases_dir)
    return '../releases/%s' % get_release_filename()

@task
def create_release_archive(head='HEAD'):
    """ Creates a local release archive """
    local('git archive --worktree-attributes --format=tar.gz %s > %s' % (
        head,
        get_release_filepath()
    ))

def sync_virtualenv(virtualenv_path, requirements_path):
    """ Updates a virtualenv with  requirements file """
    if not files.exists(virtualenv_path):
        erun('virtualenv --no-site-packages %s' % virtualenv_path)

    erun('source %s/bin/activate && pip install -r %s' % (
        virtualenv_path,
        requirements_path,
    ))

@task
def deploy(head='HEAD', requirements='requirements/production.txt'):
    """Deploy the latest version of the site to the server and restart services"""

    create_release_archive()
    release_filename = get_release_filename()

    actual_version = describe_revision(head)
    previous_version = None

    remote_path = '%(path)s/releases' % env

    release_dir = os.path.join(remote_path, 'app-%s' % describe_revision(head))
    current_release_dir = os.path.join(remote_path, 'current')
    previous_release_dir = os.path.join(remote_path, 'previous')
    virtualenv_path = os.path.abspath(os.path.join(env.path, '.virtualenv'))

    # and upload it to the server
    if not files.exists(release_dir):
        put(local_path=get_release_filepath(), remote_path=remote_path)

    try:
        # if exists remove dir
        if files.exists(release_dir):
            erun('rm -vfr %s' % (
                release_dir,
            ))
        # create the remote dir
        erun('mkdir -p %s' % release_dir)
        erun('tar xf %s -C %s' % (
            os.path.join(remote_path, release_filename),
            release_dir,
        ))
        # remove tar
        erun('rm %s' % os.path.join(remote_path, release_filename))
        # copy .env
        erun('cp %s %s' % (os.path.join(env.path, '.env'), release_dir))

        sync_virtualenv(virtualenv_path, '%s/%s' % (release_dir, requirements,))# parametrize

        with remote_virtualenv(release_dir):
            erun('python manage.py collectstatic --noinput')
            erun('python manage.py migrate')

        # find the previous release and move/unlink it
        if is_link(current_release_dir):
            # TODO: move old deploy in the 'previous' directory
            previous_deploy_path = erun('basename $(readlink -f %s)' % current_release_dir).stdout
            idx = previous_deploy_path.index('-')
            previous_version = previous_deploy_path[idx + 1:]

            if previous_version != actual_version:
                if files.exists(previous_release_dir):
                    erun('rm -R %s' % previous_release_dir)
                erun('mv %s %s' % (current_release_dir, previous_release_dir))

        erun('ln -s %s %s' % (release_dir, current_release_dir))

        restart()

        print '''
    ####################################
    #              shell               #
    ####################################
    '''
        print '''
        %s --> %s
            Use 'ps ax | grep uwsgi' to check uwsgi processes
            If first deploy run 'python manage.py createsuperuser' to create new superuser
        ''' % (previous_version, actual_version)
        open_shell('cd %s && source %s/bin/activate' % (
            current_release_dir,
            virtualenv_path,
        ))

    except CommandFailed as e:
        print 'An error occoured: %s' % e
        print '''
    ####################################
    #        fallback to shell         #
    ####################################
    '''
        print '''
        %s --> %s
            Use '../../.virtualenv/bin/uwsgi --ini uwsgi.ini' to start uwsgi
        ''' % (previous_version, actual_version)
        open_shell('cd %s && source %s/bin/activate' % (
            release_dir,
            virtualenv_path,
        ))

@task
def rollback():
  """
  Limited rollback capability. Simple loads the previously current
  version of the code. Rolling back again will swap between the two.
  """
  erun('cd %(path)s; mv releases/current releases/_previous;' % env)
  erun('cd %(path)s; mv releases/previous releases/current;' % env)
  erun('cd %(path)s; mv releases/_previous releases/previous;' %env)
  restart()

@task
def restart():
    """Restart uwsgi and web server"""
    restart_uwsgi()
    reload_server()

@task
def reload_server():
    with settings(warn_only=True):
        sudo('/etc/init.d/nginx reload')

@task
def restart_server():
    with settings(warn_only=True):
        sudo('/etc/init.d/nginx restart')

@task
def restart_uwsgi():
    """Restart uwsgi"""
    with settings(warn_only=True):
        env.virtualenv_path = os.path.abspath(os.path.join(env.path, '.virtualenv'))
        sudo('kill -9 `cat /tmp/project-master_{{ cookiecutter.repo_name }}.pid`')
        sudo('rm /tmp/project-master_{{ cookiecutter.repo_name }}.pid /tmp/uwsgi_{{ cookiecutter.repo_name }}.sock')
        erun('cd %(path)s/releases/current; %(virtualenv_path)s/bin/uwsgi -H %(virtualenv_path)s --ini %(path)s/releases/current/uwsgi.ini' % env)

def get_dump_filepath(prefix=u'backups'):
    return '../%s/%s.sql' % (prefix, get_remote_revision())

@task
def dump_db_snapshot():
    """ Dump of the production current db """
    remote_tmp_file_path = '/tmp/dump_db.sql'
    sudo('mysqldump --user {{ cookiecutter.db_user }} --password db{{ cookiecutter.repo_name }} > %s' % (remote_tmp_file_path))
    get(remote_path=remote_tmp_file_path, local_path= get_dump_filepath())

@task
def load_db_snapshot():
    """ Loads the production db snapshot in the local db """
    dump_db_snapshot()
    reset_db()
    load_db()

def reset_db():
    """ Resets the local db """
    local('python manage.py flush')

@task
def load_db():
    local('cat %s | python manage.py dbshell' % get_dump_filepath())

@task
def offline():
    """ Puts the site offline (manteinance page showed) """
    erun('cd %(path)s/releases/current; touch .maintenance;' % env)

@task
def online():
    """ Puts the site online (manteinance page removed) """
    erun('cd %(path)s/releases/current; rm .maintenance;' % env)
