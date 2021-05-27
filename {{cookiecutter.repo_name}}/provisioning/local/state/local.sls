Pyenv dependencies are installed:
  pkg.installed:
    - pkgs:
      - make
      - build-essential
      - libssl-dev
      - zlib1g-dev
      - libbz2-dev
      - libreadline-dev
      - libsqlite3-dev
      - wget
      - curl
      - llvm

Python version is present:
    pyenv.installed:
        - name: {{ pillar['python']['version'] }}
        - user: {{ pillar['filesystem']['user'] }}

Application database is present:
    postgres_database.present:
        - name: {{ pillar['database']['name'] }}
        - owner: {{ pillar['database']['owner'] }}
