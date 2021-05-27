filesystem:
    user: {{ cookiecutter.local_user }}
database:
    name: {{ cookiecutter.repo_name|replace('-', '') }}
    owner: {{ cookiecutter.local_user }}
python:
    version: {{ cookiecutter.python_version }}
