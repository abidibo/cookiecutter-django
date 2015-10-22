# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Getting Started

- clone the repository    
  `$ git clone https://github.com/{{ cookiecutter.author }}/{{ cookiecutter.repo_name }}.git`
- create a virtualenv    
  `$ virtualenv --no-site-packages .virtualenv`
- activate it    
  `$ source .venv/bin/activate`
- install requirements    
  `$ pip install -r requirements/local.txt`
- create a .env file    
  `$ touch .env`
- config environment    
  `$ dotenv set DJANGO_SETTINGS_MODULE {{ cookiecutter.repo_name }}.settings.local`    
  `$ dotenv set DB_PASSWORD <whatever>`
- run the server    
  `$ bin/runserver`
- enjoy    
  `http://localhost:8000`
