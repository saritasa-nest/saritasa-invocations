# saritasa-invocations

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/saritasa-nest/saritasa-python-invocations/checks.yml)
![PyPI](https://img.shields.io/pypi/v/saritasa-invocations)
![PyPI - Status](https://img.shields.io/pypi/status/saritasa-invocations)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/saritasa-invocations)
![PyPI - License](https://img.shields.io/pypi/l/saritasa-invocations)
![PyPI - Downloads](https://img.shields.io/pypi/dm/saritasa-invocations)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Collection of [invoke](https://www.pyinvoke.org/) commands used by Saritasa

## Table of contents

* [Installation](#installation)
* [Configuration](#configuration)
* [Modules](#modules)
  * [system](#system)
    * [system.copy-local-settings](#systemcopy-local-settings)
    * [system.copy-vscode-settings](#systemcopy-vscode-settings)
    * [system.chown](#systemchown)
    * [system.create-tmp-folder](#systemcreate-tmp-folder)
  * [git](#git)
    * [git.set-git-setting](#gitset-git-setting)
    * [git.setup](#gitsetup)
  * [pre-commit](#pre-commit)
    * [pre-commit.install](#pre-commitinstall)
    * [pre-commit.run-hooks](#pre-commitrun-hooks)
  * [docker](#docker)
    * [docker.build-service](#dockerbuild-service)
    * [docker.buildpack](#dockerbuildpack)
    * [docker.stop-all-containers](#dockerstop-all-containers)
    * [docker.up](#dockerup)
    * [docker.stop](#dockerstop)
    * [docker.clear](#dockerclear)
  * [github-actions](#github-actions)
    * [github-actions.set-up-hosts](#github-actionsset-up-hosts)
  * [python](#python)
    * [run](#pythonrun)
  * [django](#django)
    * [django.manage](#djangomanage)
    * [django.makemigrations](#djangomakemigrations)
    * [django.migrate](#djangomigrate)
    * [django.resetdb](#djangoresetdb)
    * [django.createsuperuser](#djangocreatesuperuser)
    * [django.run](#djangorun)
    * [django.shell](#djangoshell)
    * [django.dbshell](#djangodbshell)
  * [fastapi](#fastapi)
    * [fastapi.run](#fastapirun)
  * [alembic](#alembic)
    * [alembic.run](#alembicrun)
    * [alembic.autogenerate](#alembicautogenerate)
    * [alembic.upgrade](#alembicupgrade)
    * [alembic.downgrade](#alembicdowngrade)
    * [alembic.check-for-migrations](#alembiccheck-for-migrations)
    * [alembic.check-for-adjust-messages](#alembiccheck-for-adjust-messages)
  * [celery](#celery)
    * [celery.run](#celeryrun)
  * [open-api](#open-api)
    * [open-api.validate-swagger](#open-apivalidate-swagger)

## Installation

```bash
pip install saritasa-invocations
```

or if you are using [poetry](https://python-poetry.org/)

```bash
poetry add saritasa-invocations
```

## Configuration

Configuration can be set in `tasks.py` file.

Below is an example of config:

```python
from invoke import Collection

from saritasa_invocations import (
    docker,
    git,
    github_actions,
    pre_commit,
    system,
)

ns = Collection(
    docker,
    git,
    github_actions,
    pre_commit,
    system,
)

# Configurations for run command
ns.configure(
    dict(
        run=dict(
            pty=True,
            echo=True,
        ),
        saritasa_invocations={
            "pre_commit_hooks": (
                "pre-commit",
                "pre-push",
                "commit-msg",
            ),
            "merge_ff": "true",
            "pull_ff": "only",
            "docker_main_containers": (
                "opensearch",
                "redis",
            ),
            "vs_code_settings_template": ".vscode/recommended_settings.json",
            "settings_template": "config/.env.local",
            "save_settings_from_template_to": "config/.env",
        },
    ),
)
```

## Modules

### system

#### system.copy-local-settings

Copies local template for settings into specified file

Settings:

* `settings_template` path to settings template (Default: `config/settings/local.template.py`)
* `save_settings_from_template_to` path to where save settings (Default: `config/settings/local.py`)

#### system.copy-vscode-settings

Copies local template for vscode settings into `.vscode` folder

Settings:

* `vs_code_settings_template` path to settings template (Default: `.vscode/recommended_settings.json`)

#### system.chown

Change owner ship of project files to current user.

Shortcut for owning apps dir by current user after some files were
generated using docker-compose (migrations, new app, etc).

#### system.create-tmp-folder

Create folder for temporary files(`.tmp`).

### git

#### git.set-git-setting

Set git setting in config

#### git.setup

Preform setup of git:

* Install pre-commit hooks
* Set merge.ff
* Set pull.ff

Settings:

* `merge_ff` setting value for `merge.ff` (Default: `false`)
* `pull_ff` setting value for `pull.ff` (Default: `only`)

### pre-commit

#### pre-commit.install

Install git hooks via pre-commit.

Settings:

* `pre_commit_hooks` list of hooks to install (Default: `["pre-commit", "pre-push", "commit-msg"]`)

#### pre-commit.run-hooks

Run all hooks against all files

### docker

#### docker.build-service

Build service image from docker compose

#### docker.buildpack

Build project via [pack-cli](https://buildpacks.io/docs/tools/pack/)

Settings:

* `buildpack_builder` image tag of builder (Default: `paketobuildpacks/builder:base`)
* `buildpack_runner` image tag of runner (Default: `paketobuildpacks/run:base`)
* `build_image_tag` image tag of builder (Default: Name of project from `project_name`)
* `buildpack_requirements_path` path to folder with requirements (Default: `requirements`)

#### docker.stop-all-containers

Shortcut for stopping ALL running docker containers

#### docker.up

Bring up main containers and start them.

Settings:

* `docker_main_containers` image tag of builder (Default: `["postgres", "redis"]`)

#### docker.stop

Stop main containers.

Settings:

* `docker_main_containers` image tag of builder (Default: `["postgres", "redis"]`)

#### docker.clear

Stop and remove all containers defined in docker-compose. Also remove images.

### github-actions

#### github-actions.set-up-hosts

Add hosts to `/etc/hosts`.

Settings:

* `github_action_hosts` image tag of builder (Default: see `docker-main-containers`)

### python

As of now we support two environments for python `local` and `docker`.

* `local` is a python that is located in your current virtualenv
* `docker` is python that is located inside your docker image of service (`python_docker_service`).

This was done to have ability to run code against environment close deployed one or simply test it out.

Example of usage

```bash
PYTHON_ENV=docker inv python.run-python --command="--version"
```

#### python.run

Run python command depending on `PYTHON_ENV` variable(`docker` or `local`).

Settings:

* `python_entry` python entry command (Default: `python`)
* `python_docker_service` python service name (Default: `web`)
* `python_docker_service_params` params for docker (Default: `--rm`)

### django

#### django.manage

Run `manage.py` with specified command.

This command also handle starting of required services and waiting DB to
be ready.

Requires [django_probes](https://github.com/painless-software/django-probes#basic-usage)

#### django.makemigrations

Run `makemigrations` command and chown created migrations (only for docker env).

#### django.check_new_migrations

Check if there is new migrations or not. Result should be check via exit code.

#### django.migrate

Run `migrate` command.

Settings:

* `django_migrate_command` migrate command (Default: `migrate`)

#### django.resetdb

Reset database to initial state (including test DB).

Requires [django-extensions](https://django-extensions.readthedocs.io/en/latest/installation_instructions.html)

#### django.createsuperuser

Create superuser.

Settings:

* `default_superuser_email` default email of superuser (Default: `root@localhost`)
* `default_superuser_username` default username of superuser (Default: `root`)
* `default_superuser_password` default password of superuser (Default: `root`)

#### django.run

Run development web-server.

Settings:

* `runserver_docker_params` params for docker (Default: `--rm --service-ports`)
* `runserver_command` runserver command (Default: `runserver_plus`)
* `runserver_host` host of server (Default: `0.0.0.0`)
* `runserver_port` port of server (Default: `8000`)
* `runserver_params` params for runserver command (Default: `""`)

#### django.shell

Shortcut for manage.py shell command.

Settings:

* `shell_command` command to start python shell (Default: `shell_plus --ipython`)

#### django.dbshell

Open database shell with credentials from current django settings.

### fastapi

#### fastapi.run

Run development web-server.

Settings:

* `fastapi_docker_params` params for docker (Default: `--rm --service-ports`)
* `fastapi_uvicorn_command` uvicorn command (Default: `-m uvicorn`)
* `fastapi_app` path to fastapi app (Default: `config:fastapi_app`)
* `fastapi_host` host of server (Default: `0.0.0.0`)
* `fastapi_port` port of server (Default: `8000`)
* `fastapi_params` params for uvicorn (Default: `--reload`)

### alembic

#### alembic.run

Run alembic command

Settings:

* `alembic_command` alembic command (Default: `-m alembic`)

#### alembic.autogenerate

Generate migrations

Settings:

* `alembic_migrations_folder` migrations files location (Default: `db/migrations/versions`)

#### alembic.upgrade

Upgrade database

#### alembic.downgrade

Downgrade database

#### alembic.check-for-migrations

Check if there any missing migrations to be generated

#### alembic.check-for-adjust-messages

Check migration files for adjust messages

Settings:

* `alembic_migrations_folder` migrations files location (Default: `db/migrations/versions`)
* `alembic_adjust_messages` list of alembic adjust messages (Default: `# ### commands auto generated by Alembic - please adjust! ###`, `# ### end Alembic commands ###`)

### celery

#### celery.run

Start celery worker.

Settings:

* `celery_local_cmd` command for celery (Default: `celery --app config.celery:app worker --beat --scheduler=django --loglevel=info`)
* `celery_service_name` name of celery service (Default: `celery`)

### open-api

#### open-api.validate-swagger

Check that generated open_api spec is valid. This command uses
[drf-spectacular](https://github.com/tfranzel/drf-spectacular) and
it's default validator. It creates spec file in ./tmp folder and then validates it.
