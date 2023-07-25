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

#### copy-local-settings

Copies local template for settings into specified file

Settings:
* `settings_template` path to settings template (Default: `config/settings/local.template.py`)
* `save_settings_from_template_to` path to where save settings (Default: `config/settings/local.py`)

#### copy-local-settings

Copies local template for vscode settings into `.vscode` folder

Settings:
* `vs_code_settings_template` path to settings template (Default: `.vscode/recommended_settings.json`)

#### chown

Change owner ship of project files to current user.

Shortcut for owning apps dir by current user after some files were
generated using docker-compose (migrations, new app, etc).

#### create-tmp-folder

Create folder for temporary files(`.tmp`).

### git

#### set-git-setting

Set git setting in config

#### setup

Preform setup of git:

* Install pre-commit hooks
* Set merge.ff
* Set pull.ff

Settings:
* `merge_ff` setting value for `merge.ff` (Default: `false`)
* `pull_ff` setting value for `pull.ff` (Default: `only`)

### pre-commit

#### install

Install git hooks via pre-commit.

Settings:
* `pre_commit_hooks` list of hooks to install (Default: `["pre-commit", "pre-push", "commit-msg"]`)

#### run-hooks

Run all hooks against all files

### docker

#### build-service

Build service image from docker compose

#### buildpack

Build project via [pack-cli](https://buildpacks.io/docs/tools/pack/)

Settings:
* `buildpack_builder` image tag of builder (Default: `paketobuildpacks/builder:base`)
* `buildpack_runner` image tag of runner (Default: `paketobuildpacks/run:base`)
* `build_image_tag` image tag of builder (Default: Name of project from `project_name`)
* `buildpack_requirements_path` path to folder with requirements (Default: `requirements`)

#### stop-all-containers

Shortcut for stopping ALL running docker containers

#### up

Bring up main containers and start them.

Settings:
* `docker_main_containers` image tag of builder (Default: `["postgres", "redis"]`)

#### stop

Stop main containers.

Settings:
* `docker_main_containers` image tag of builder (Default: `["postgres", "redis"]`)

#### clear

Stop and remove all containers defined in docker-compose. Also remove images.

### github-actions

#### set-up-host

Set up host in `/etc/hosts`

#### set-up-hosts

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

#### run_python

Run python command depending on `PYTHON_ENV` variable(`docker` or `local`).

Settings:
* `python_entry` python entry command (Default: `python`)
* `python_docker_service` python service name (Default: `web`)
* `python_docker_service_params` params for docker (Default: `--rm`)

### django

#### manage

Run `manage.py` with specified command.

This command also handle starting of required services and waiting DB to
be ready.

Requires [django_probes](https://github.com/painless-software/django-probes#basic-usage)

#### makemigrations

Run `makemigrations` command and chown created migrations (only for docker env).

#### check_new_migrations

Check if there is new migrations or not. Result should be check via exit code.

#### migrate

Run `migrate` command.

Settings:
* `django_migrate_command` migrate command (Default: `migrate`)

#### resetdb

Reset database to initial state (including test DB).

Requires [django-extensions](https://django-extensions.readthedocs.io/en/latest/installation_instructions.html)


#### createsuperuser

Create superuser.

Settings:
* `default_superuser_email` default email of superuser (Default: `root@localhost`)
* `default_superuser_username` default username of superuser (Default: `root`)
* `default_superuser_password` default password of superuser (Default: `root`)

#### run

Run development web-server.

Settings:
* `runserver_docker_params` params for docker (Default: `--rm --service-ports`)
* `runserver_command` runserver command (Default: `runserver_plus`)
* `runserver_host` host of server (Default: `0.0.0.0`)
* `runserver_port` port of server (Default: `8000`)
* `runserver_params` params for runserver command (Default: `""`)

#### shell

Shortcut for manage.py shell command.

Settings:
* `shell_command` command to start python shell (Default: `shell_plus --ipython`)

#### dbshell

Open database shell with credentials from current django settings.

### fastapi

#### run

Run development web-server.

Settings:
* `fastapi_docker_params` params for docker (Default: `--rm --service-ports`)
* `fastapi_uvicorn_command` uvicorn command (Default: `-m uvicorn`)
* `fastapi_app` path to fastapi app (Default: `config:fastapi_app`)
* `fastapi_host` host of server (Default: `0.0.0.0`)
* `fastapi_port` port of server (Default: `8000`)
* `fastapi_params` params for uvicorn (Default: `--reload`)


### celery

#### run

Start celery worker.

Settings:
* `celery_local_cmd` command for celery (Default: `celery --app config.celery:app worker --beat --scheduler=django --loglevel=info`)
* `celery_service_name` name of celery service (Default: `celery`)

### open-api

#### validate-swagger

Check that generated open_api spec is valid. This command uses
[drf-spectacular](https://github.com/tfranzel/drf-spectacular) and
it's default validator. It creates spec file in ./tmp folder and then validates it.
