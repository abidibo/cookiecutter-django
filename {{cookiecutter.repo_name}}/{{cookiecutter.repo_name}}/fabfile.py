from fabric.api import *
# Default release is 'current'
env.release = 'current'

def production():
  """Production server settings"""
  env.settings = 'production'
  env.user = '{{ cookiecutter.remote_user }}'
  env.path = '/home/%(user)s/sites/{{ cookiecutter.repo_name }}' % env
  env.hosts = ['{{ cookiecutter.domain }}']

def setup():
  """
  Setup a fresh virtualenv and install everything we need so it's ready to deploy to
  """
  run('mkdir -p %(path)s; cd %(path)s; virtualenv --no-site-packages .; mkdir releases; mkdir shared;' % env)
  clone_repo()
  checkout_latest()
  install_requirements()

def deploy():
  """Deploy the latest version of the site to the server and restart nginx"""
  checkout_latest()
  install_requirements()
  symlink_current_release()
  migrate()
  restart_server()

def clone_repo():
  """Do initial clone of the git repo"""
  run('cd %(path)s; git clone /home/%(user)s/git/repositories/{{ cookiecutter.repo_name }}.git repository' % env)

def checkout_latest():
  """Pull the latest code into the git repo and copy to a timestamped release directory"""
  import time
  env.release = time.strftime('%Y%m%d%H%M%S')
  run("cd %(path)s/repository; git pull origin deployment" % env)
  run('cp -R %(path)s/repository %(path)s/releases/%(release)s; rm -rf %(path)s/releases/%(release)s/.git*' % env)

def install_requirements():
  """Install the required packages using pip"""
  run('cd %(path)s; %(path)s/bin/pip install -r ./releases/%(release)s/requirements.txt --allow-external PIL --allow-unverified PIL' % env)

def symlink_current_release():
  """Symlink our current release, uploads and settings file"""
  with settings(warn_only=True):
    run('cd %(path)s; rm releases/previous; mv releases/current releases/previous;' % env)
  run('cd %(path)s; ln -s %(release)s releases/current' % env)
  """ production settings"""
  run('cd %(path)s/releases/current/; cp settings_%(settings)s.py torinometeo/settings.py' % env)
  with settings(warn_only=True):
    run('rm %(path)s/shared/static' % env)
    run('cd %(path)s/releases/current/static/; ln -s %(path)s/releases/%(release)s/static %(path)s/shared/static ' %env)

def migrate():
  """Run our migrations"""
  run('cd %(path)s/releases/current; ../../bin/python manage.py migrate --noinput --settings=settings.production' % env)

def rollback():
  """
  Limited rollback capability. Simple loads the previously current
  version of the code. Rolling back again will swap between the two.
  """
  run('cd %(path)s; mv releases/current releases/_previous;' % env)
  run('cd %(path)s; mv releases/previous releases/current;' % env)
  run('cd %(path)s; mv releases/_previous releases/previous;' %env)
  restart_server()

def restart_server():
  """Restart the web server"""
  with settings(warn_only=True):
    sudo('kill -9 `cat /tmp/project-master_{{ cookiecutter.repo_name }}.pid`')
    sudo('rm /tmp/project-master_{{ cookiecutter.repo_name }}.pid /tmp/uwsgi_{{ cookiecutter.repo_name }}.sock')
  run('cd %(path)s/releases/current; %(path)s/bin/uwsgi --ini %(path)s/releases/current/uwsgi.ini' % env)
  sudo('/etc/init.d/nginx restart')
