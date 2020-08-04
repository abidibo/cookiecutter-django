import os
import sys
import time
import threading

from dotenv import load_dotenv  # type: ignore
from getenv import env  # type: ignore
from fabric import Connection, task  # type: ignore
from patchwork import files  # type: ignore
from invoke import Responder  # type: ignore


def here(*args):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), *args)


dotenv_path = here('.env')
load_dotenv(dotenv_path)


class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in '|/-\\':
                yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay):
            self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        d = threading.Thread(target=self.spinner_task)
        d.start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False


class bcolors:
    HEADER = '\033[1m\033[33m'
    INFO = '\033[94m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_(text, color):
    print(getattr(bcolors, color) + text + bcolors.ENDC + (bcolors.ENDC if color == 'HEADER' else ''))  # noqa


def get_env(ctx, var=None):
    if var is None:
        return ctx.config.run.env
    return ctx.config.run.env[var]


def set_env(ctx, var, val):
    ctx.config.run.env[var] = val


def get_connection(ctx):
    return ctx.config.run.env['conn']


def sudo_responder(ctx):
    return Responder(
        pattern=r'\[sudo\] password',
        response=f"{get_env(ctx, 'sudo_password')}\n"
    )


def db_password_responder(ctx):
    return Responder(
        pattern=r'Enter password',
        response=f"{get_env(ctx, 'db_password')}\n"
    )


def describe_revision(ctx, head='HEAD', log=True):
    """ Describes the current local revision """
    c = get_connection(ctx)
    result = c.local(f"git describe --always {head}", hide=True)
    tag = result.stdout.rstrip()
    if log:
        print(f"Current tag of {head}: {tag}")
    return tag


def get_release_filename(ctx, head='HEAD', log=True):
    return f"{describe_revision(ctx, head, log)}.tar.gz"


def get_release_filepath(ctx, head='HEAD', log=True):
    releases_dir = here('..', 'releases')
    if not os.path.exists(releases_dir):
        os.makedirs(releases_dir)
    return '../releases/%s' % get_release_filename(ctx, head, log)


def sync_virtualenv(ctx, virtualenv_path, requirements_path):
    """ Updates a virtualenv with requirements file """
    c = get_connection(ctx)
    if not files.exists(c, virtualenv_path):
        c.run(f"python3 -m venv {virtualenv_path}")

    result = c.run(f"source {virtualenv_path}/bin/activate && pip install -r {requirements_path}", hide='stdout')  # noqa
    counter = 0
    for line in result.stdout.split('\n'):
        if not line.startswith('Requirement already satisfied'):
            counter += 1
            print(line)
    if counter == 0:
        print('All requirements already satisfied')


def get_dump_filepath(ctx, prefix=u'backups', log=True):
    return f"../{prefix}/{getRemoteRevision(ctx, log)}.sql"


def reset_db(ctx):
    """ Resets the local db """
    c = get_connection(ctx)
    print_('Flushing local db', 'INFO')
    c.local(f"source {here('..', '.virtualenv', 'bin', 'activate')} && python manage.py flush")
    print_('Done!', 'SUCCESS')


@task
def production(ctx):
    """ Production server settings """
    ctx.config.run.env['path'] = '{{ cookiecutter.webapp_dir }}'
    ctx.config.run.env['conn'] = Connection(
        host='{{ cookiecutter.domain }}', user='{{ cookiecutter.remote_user }}')
    ctx.config.run.env['db_password'] = env('REMOTE_DB_PWD')
    ctx.config.run.env['sudo_password'] = env('REMOTE_USER_PWD')


@task
def createReleaseArchive(ctx, head='HEAD'):
    """ Creates a local release archive """
    print_("Creating release archive", 'INFO')
    c = get_connection(ctx)
    c.local('git archive --worktree-attributes --format=tar.gz {0} > {1}'.format(  # noqa
        head,
        get_release_filepath(ctx, head)
    ))
    print_("Done!", 'SUCCESS')


@task
def deploy(ctx, head='HEAD', requirements='requirements/production.txt'):
    """ Deploy the latest version of the site to the server and
        restart services """
    print_("Running task 'deploy'", 'HEADER')
    print('Creates a new release, uploads it to the remote server, updates packages, runs migrations and restarts services.')  # noqa
    print("...")

    c = get_connection(ctx)

    # create archive
    createReleaseArchive(ctx)
    release_filename = get_release_filename(ctx, log=False)
    current_version = describe_revision(ctx, log=False)
    previous_version = None

    print_('Uploading new release to remote server', 'INFO')
    remote_path = f"{get_env(ctx, 'path')}/releases"
    print(f"Remote releases folder path: {remote_path}")
    release_dir = os.path.join(remote_path, f"app-{current_version}")
    print(f"Remote new release directory: {release_dir}")
    current_release_dir = os.path.join(remote_path, 'current')
    previous_release_dir = os.path.join(remote_path, 'previous')
    virtualenv_path = os.path.abspath(os.path.join(get_env(ctx, 'path'), '.virtualenv'))  # noqa
    print(f"Remote virtualenv path: {virtualenv_path}")

    # and upload it to the server
    if not files.exists(c, release_dir):
        print('Uploading package, be patient')
        with Spinner():
            c.put(get_release_filepath(ctx, head, False), remote=remote_path)
            print()
            print_('Done!', 'SUCCESS')
    else:
        print('Release package already uploaded')
        print_('Done!', 'SUCCESS')

    try:
        # if exists remove dir
        if files.exists(c, release_dir):
            c.run(f"rm -vfr {release_dir}", hide='stdout')
        # create the remote dir
        c.run(f"mkdir -p {release_dir}")
        print_('Unzip package', 'INFO')
        c.run(f"tar xf {os.path.join(remote_path, release_filename)} -C {release_dir}")  # noqa
        # remove tar
        c.run(f"rm {os.path.join(remote_path, release_filename)}", hide='stdout')  # noqa
        print_('Done!', 'SUCCESS')
        # copy .env
        print_('Copying env file', 'INFO')
        c.run(f"cp {os.path.join(get_env(ctx, 'path'), '.env')} {release_dir}")
        print_('Done!', 'SUCCESS')

        print_('Syncing virtualenv', 'INFO')
        sync_virtualenv(ctx, virtualenv_path, f"{release_dir}/{requirements}")
        print_('Done!', 'SUCCESS')

        print_('Collecting static files', 'INFO')
        c.run(f"cd {release_dir} && source {virtualenv_path}/bin/activate && python manage.py collectstatic --noinput", hide='stdout')
        print_('Done!', 'SUCCESS')
        print_('Running migrations', 'INFO')
        c.run(f"cd {release_dir} && source {virtualenv_path}/bin/activate && python manage.py migrate")  # noqa
        print_('Done!', 'SUCCESS')

        print_('Setting current/previous releases', 'INFO')
        # find the previous release and move/unlink it
        if files.exists(c, current_release_dir):
            previous_deploy_path = c.run(f"basename $(readlink -f {current_release_dir})", hide='stdout').stdout.rstrip()
            idx = previous_deploy_path.index('-')
            previous_version = previous_deploy_path[idx + 1:]

            if previous_version != current_version:
                if files.exists(c, previous_release_dir):
                    c.run(f"rm -R {previous_release_dir}")
                c.run(f"mv {current_release_dir} {previous_release_dir}")

        c.run(f"ln -s {release_dir} {current_release_dir}")
        print_('Done!', 'SUCCESS')

        restart(ctx)

        print()
        print_('Shell', 'HEADER')
        print('You\'re now on the remote server with the virtualenv activated, you can make some good stuff if you want...')
        print('''
        %s --> %s
            Use 'ps ax | grep uwsgi' to check uwsgi processes
            If first deploy run 'python manage.py createsuperuser' to create new superuser
        ''' % (previous_version, current_version))
        c.run(f"cd {release_dir} && source {virtualenv_path}/bin/activate && /bin/bash", pty=True)

    except Exception as e:
        print_(f"An error occoured: {str(e)}", 'WARNING')
        print_('Fallback to shell', 'HEADER')
        print('''
        %s --> %s
            Use '../../.virtualenv/bin/uwsgi --ini uwsgi.ini' to start uwsgi
        ''' % (previous_version, current_version))
        c.run(f"cd {release_dir} && source {virtualenv_path}/bin/activate && /bin/bash", pty=True)


@task
def rollback(ctx):
    """
    Limited rollback capability. Simple loads the previously current
    version of the code. Rolling back again will swap between the two.
    """
    print_("Running task 'rollback'", 'HEADER')
    print('Swaps previous and current releases')  # noqa
    print("...")
    c = get_connection(ctx)
    print_('Swapping folders', 'INFO')
    path = get_env(ctx, 'path')
    c.run(f"cd {path}; mv releases/current releases/_previous;")
    c.run(f"cd {path}; mv releases/previous releases/current;")
    c.run(f"cd {path}; mv releases/_previous releases/previous;")
    print_('Done!', 'SUCCESS')
    restart(ctx)


@task
def getRemoteRevision(ctx, log=True):
    """ Returns and prints the current deployed remote revision """
    c = get_connection(ctx)
    if log:
        print_('Getting remote current revision', 'INFO')
    current_app_dir = c.run(f"basename $(readlink -f {get_env(ctx, 'path')}/releases/current)", hide='stdout').stdout.rstrip()  # noqa
    try:
        _, remote_revision = current_app_dir.split('-')
    except Exception as e:
        print_(str(e), 'FAIL')
        remote_revision = 'unknown'

    if log:
        print(f"Current remote revision: {remote_revision}")
        print_('Done!', 'SUCCESS')
    return remote_revision


@task
def dumpDbSnapshot(ctx):
    """ Dump of the production current db """
    print_("Dumping remote db", 'INFO')
    remote_tmp_file_path = '/tmp/dump_db.sql'
    c = get_connection(ctx)
    c.local(f"mkdir -p {here('..', 'backups')}")
    c.run(f"mysqldump --user {{ cookiecutter.db_user }} --password db{{ cookiecutter.repo_name }} > {remote_tmp_file_path}",  # noqa
          pty=True,
          watchers=[db_password_responder(ctx)])

    print_('Downloading db snapshot', 'INFO')
    with Spinner():
        c.get(remote_tmp_file_path, local=get_dump_filepath(ctx, log=False))
        print()
        print_('Done!', 'SUCCESS')


@task
def loadDbSnapshot(ctx):
    """ Loads the production db snapshot in the local db """
    print_("Running task 'loadDbSnapshot'", 'HEADER')
    print("Dumps and download the current remote db snapshot and loads it in the local db")  # noqa
    print("...")

    dumpDbSnapshot(ctx)
    reset_db(ctx)
    loadDb(ctx)


@task
def loadDb(ctx):
    """ Loads the downloaded production db snapshot in the local db """
    c = get_connection(ctx)
    print_('Loading db snapshot', 'INFO')
    c.local(f"source {here('..', '.virtualenv', 'bin', 'activate')} && cat {get_dump_filepath(ctx, log=False)} | python manage.py dbshell")  # noqa
    print_('Done!', 'SUCCESS')


@task
def offline(ctx):
    """ Puts the site offline (manteinance page showed) """
    print_("Running task 'offline'", 'HEADER')
    print("Puts the site in maintenance mode")  # noqa
    print("...")
    c = get_connection(ctx)
    print_('Creating maintenance file', 'INFO')
    c.run(f"cd {get_env(ctx, 'path')}/releases/current; touch .maintenance;")
    print_('Done!', 'SUCCESS')


@task
def online(ctx):
    """ Puts the site online (manteinance page removed) """
    print_("Running task 'online'", 'HEADER')
    print("Exits from maintenance mode")  # noqa
    print("...")
    c = get_connection(ctx)
    print_('Removing maintenance file', 'INFO')
    c.run(f"cd {get_env(ctx, 'path')}/releases/current; rm .maintenance;")
    print_('Done!', 'SUCCESS')


@task
def reloadServer(ctx):
    """ Reload the web server """
    print_("Reloading web server...", 'INFO')
    c = get_connection(ctx)
    c.sudo(
        '/etc/init.d/nginx reload',
        pty=True,
        hide='stdout',
        watchers=[sudo_responder(ctx)])
    print_("Done!", 'SUCCESS')


@task
def restart_uwsgi(ctx):
    """ Restart uWSGI """
    print_("Restarting uWSGI...", 'INFO')
    c = get_connection(ctx)
    set_env(ctx, 'virtualenv_path',
            os.path.abspath(os.path.join(get_env(ctx, 'path'), '.virtualenv')))
    c.run('kill -9 `cat /tmp/project-master_{{ cookiecutter.repo_name }}.pid`', warn=True)
    c.run('rm /tmp/project-master_{{ cookiecutter.repo_name }}.pid /tmp/uwsgi_{{ cookiecutter.repo_name }}.sock', warn=True)  # noqa
    c.run('cd %(path)s/releases/current; %(virtualenv_path)s/bin/uwsgi -H %(virtualenv_path)s --ini %(path)s/releases/current/uwsgi.ini' % get_env(ctx)) # noqa
    print_("Done!", 'SUCCESS')


@task
def restart(ctx):
    """ Restart services and application """
    print_("Running task 'restart'", 'HEADER')
    print("Restarts the application layer and reloads the web server")
    print("...")
    restart_uwsgi(ctx)
    reloadServer(ctx)
