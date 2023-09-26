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
  * [printing](#printing)
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
    * [pre-commit.update](#pre-commitupdate)
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
    * [django.django.recompile-messages](#djangorecompile-messages)
    * [django.load-db-dump](#djangoload-db-dump)
    * [django.backup-local-db](#djangobackup-local-db)
    * [django.backup-remote-db](#djangobackup-remote-db)
    * [django.load-remote-db](#djangoload-remote-db)
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
  * [db](#db)
    * [db.load-db-dump](#dbload-db-dump)
    * [db.backup-local-db](#dbbackup-local-db)
  * [k8s](#k8s)
    * [k8s.login](#k8slogin)
    * [k8s.set-context](#k8sset-context)
    * [k8s.logs](#k8slogs)
    * [k8s.pods](#k8spods)
    * [k8s.execute](#k8sexecute)
    * [k8s.python-shell](#k8spython-shell)
    * [k8s.health-check](#k8shealth-check)
    * [k8s.download-file](#k8sdownload-file)
  * [db-k8s](#db-k8s)
    * [db-k8s.create-dump](#db-k8screate-dump)
    * [db-k8s.get-dump](#db-k8sget-dump)
  * [cruft](#cruft)
    * [cruft.check-for-cruft-files](#cruftcheck-for-cruft-files)
    * [cruft.create_project](#cruftcreate_project)
  * [poetry](#poetry)
    * [poetry.install](#poetryinstall)
    * [poetry.update](#poetryupdate)
    * [poetry.update-to-latest](#poetryupdate-to-latest)
  * [pip](#pip)
    * [pip.install-dependencies](#pipinstall-dependencies)
    * [pip.compile](#pipcompile-dependencies)
  * [mypy](#mypy)
    * [mypy](#mypyrun)
  * [pytest](#pytest)
    * [pytest](#pytestrun)

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
import invoke

import saritasa_invocations

ns = invoke.Collection(
    saritasa_invocations.docker,
    saritasa_invocations.git,
    saritasa_invocations.github_actions,
    saritasa_invocations.pre_commit,
    saritasa_invocations.system,
)

# Configurations for run command
ns.configure(
    {
        "run": {
            "pty": True,
            "echo": True,
        },
        "saritasa_invocations": saritasa_invocations.Config(
            pre_commit=saritasa_invocations.PreCommitSettings(
                hooks=(
                    "pre-commit",
                    "pre-push",
                    "commit-msg",
                )
            ),
            git=saritasa_invocations.GitSettings(
                merge_ff="true",
                pull_ff="only",
            ),
            docker=saritasa_invocations.DockerSettings(
                main_containers=(
                    "opensearch",
                    "redis",
                ),
            ),
            system=saritasa_invocations.SystemSettings(
                vs_code_settings_template=".vscode/recommended_settings.json",
                settings_template="config/.env.local",
                save_settings_from_template_to="config/.env",
            ),
            # Default K8S Settings shared between envs
            k8s_defaults=saritasa_invocations.K8SDefaultSettings(
                proxy="teleport.company.com",
                db_config=saritasa_invocations.K8SDBSettings(
                    namespace="db",
                    pod_selector="app=pod-selector-db",
                ),
            )
        ),
    },
)

# For K8S settings you just need to create a instances of K8SSettings for each
# environnement. It'll be all collected automatically.
saritasa_invocations.K8SSettings(
    name="dev",
    cluster="teleport.company.somewhere.com",
    namespace="project_name",
)
saritasa_invocations.K8SSettings(
    name="prod",
    cluster="teleport.client.somewhere.com",
    namespace="project_name",
    proxy="teleport.client.com",
)
```

## Modules

### printing

While this module doesn't contain any invocations, it's used to print message
via `rich.panel.Panel`. There are three types:

* `print_success` - print message in green panel
* `print_warning` - print message in yellow panel
* `print_error` - print message in red panel

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

* `hooks` list of hooks to install (Default: `["pre-commit", "pre-push", "commit-msg"]`)

#### pre-commit.run-hooks

Run all hooks against all files.

#### pre-commit.update

Update pre-commit dependencies.

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

#### docker.pull

Pull images associated with main containers.

Settings:

* `pull_params` params for docker pull command (Default: `--quiet`)

#### docker.up

Bring up main containers and start them.

Settings:

* `main_containers` image tag of builder (Default: `["postgres", "redis"]`)

#### docker.stop

Stop main containers.

Settings:

* `main_containers` image tag of builder (Default: `["postgres", "redis"]`)

#### docker.clear

Stop and remove all containers defined in docker-compose. Also remove images.

### github-actions

#### github-actions.set-up-hosts

Add hosts to `/etc/hosts`.

Settings:

* `hosts` image tag of builder (Default: see `docker-main-containers`)

### python

As of now we support two environments for python `local` and `docker`.

* `local` is a python that is located in your current virtualenv
* `docker` is python that is located inside your docker image of service (`python_docker_service`).

This was done to have ability to run code against environment close deployed one or simply test it out.

Example of usage

```bash
PYTHON_ENV=docker inv python.run --command="--version"
```

#### python.run

Run python command depending on `PYTHON_ENV` variable(`docker` or `local`).

Settings:

* `entry` python entry command (Default: `python`)
* `docker_service` python service name (Default: `web`)
* `docker_service_params` params for docker (Default: `--rm`)

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

* `migrate_command` migrate command (Default: `migrate`)

#### django.resetdb

Reset database to initial state (including test DB).

Requires [django-extensions](https://django-extensions.readthedocs.io/en/latest/installation_instructions.html)

Settings:

* `django_settings_path` default django settings (Default: `config.settings.local`)

#### django.createsuperuser

Create superuser.

Settings:

* `default_superuser_email` default email of superuser (Default: `root@localhost`)
* `default_superuser_username` default username of superuser (Default: `root`)
* `default_superuser_password` default password of superuser (Default: `root`)
* `verbose_email_name` verbose name for `email` field (Default: `Email address`)
* `verbose_username_name` verbose name for `username` field (Default: `Username`)
* `verbose_password_name` verbose name for `password` field (Default: `Password`)

Note:

* Values for `verbose_email_name`, `verbose_username_name`, `verbose_password_name`
should match with verbose names of model that used
[this setting](https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#substituting-a-custom-user-model)

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

#### django.recompile-messages

Generate and recompile translation messages.

Requires [gettext](https://www.gnu.org/software/gettext/)

Settings:

* `makemessages_params` params for makemessages command (Default: `--all --ignore venv`)
* `compilemessages_params` params for compilemessages command (Default: `""`)

#### django.load-db-dump

Reset db and load db dump.

Uses [resetdb](#djangoresetdb) and [load-db-dump](#dbload-db-dump)

Settings:

* `django_settings_path` default django settings (Default: `config.settings.local`)

#### django.backup-local-db

Back up local db.

Uses [backup_local_db](#dbbackup-local-db)

Settings:

* `django_settings_path` default django settings (Default: `config.settings.local`)

#### django.backup-remote-db

Make dump of remote db and download it.

Uses [create_dump](#db-k8screate-dump) and [get-dump](#db-k8sget-dump)

Settings:

* `django_settings_path` default django settings (Default: `config.settings.local`)

#### django.load-remote-db

Make dump of remote db and download it and apply to local db.

Uses [create_dump](#db-k8screate-dump) and [get-dump](#db-k8sget-dump) and
[load-db-dump](#djangoload-db-dump)

Settings:

* `django_settings_path` default django settings (Default: `config.settings.local`)

### fastapi

#### fastapi.run

Run development web-server.

Settings:

* `docker_params` params for docker (Default: `--rm --service-ports`)
* `uvicorn_command` uvicorn command (Default: `-m uvicorn`)
* `app` path to fastapi app (Default: `config:fastapi_app`)
* `host` host of server (Default: `0.0.0.0`)
* `port` port of server (Default: `8000`)
* `params` params for uvicorn (Default: `--reload`)

### alembic

#### alembic.run

Run alembic command

Settings:

* `command` alembic command (Default: `-m alembic`)
* `connect_attempts` numbers of attempts to connect to database (Default: `10`)

#### alembic.autogenerate

Generate migrations

Settings:

* `migrations_folder` migrations files location (Default: `db/migrations/versions`)

#### alembic.upgrade

Upgrade database

#### alembic.downgrade

Downgrade database

#### alembic.check-for-migrations

Check if there any missing migrations to be generated

#### alembic.check-for-adjust-messages

Check migration files for adjust messages

Settings:

* `migrations_folder` migrations files location (Default: `db/migrations/versions`)
* `adjust_messages` list of alembic adjust messages (Default: `# ### commands auto generated by Alembic - please adjust! ###`, `# ### end Alembic commands ###`)

### celery

#### celery.run

Start celery worker.

Settings:

* `local_cmd` command for celery (Default: `celery --app config.celery:app worker --beat --scheduler=django --loglevel=info`)
* `service_name` name of celery service (Default: `celery`)

### open-api

#### open-api.validate-swagger

Check that generated open_api spec is valid. This command uses
[drf-spectacular](https://github.com/tfranzel/drf-spectacular) and
it's default validator. It creates spec file in ./tmp folder and then validates it.

### db

#### db.load-db-dump

Load db dump to local db.

Settings:

* `load_dump_command` template for load command(Default located in `_config.pp > dbSettings`)
* `dump_filename` filename for dump (Default: `local_db_dump`)
* `load_additional_params` additional params for load command (Default: `--quite`)

#### db.backup-local-db

Back up local db.

Settings:

* `dump_command` template for dump command (Default located in `_config.pp > dbSettings`)
* `dump_filename` filename for dump (Default: `local_db_dump`)
* `dump_additional_params` additional params for dump command (Default: `--no-owner`)

### k8s

For K8S settings you just need to create a instances of `K8SSettings` for each
environnement. It'll be all collected automatically.

#### k8s.login

Login into k8s via teleport.

Settings:

* `proxy` teleport proxy (**REQUIRED**)
* `port` teleport port (Default: `443`)
* `auth` teleport auth method (Default: `github`)

#### k8s.set-context

Set k8s context to current project

Settings:

* `namespace` namespace for k8s (Default: Name of project from `project_name`)

#### k8s.logs

Get logs for k8s pod

Settings:

* `default_component` default component (Default: `backend`)

#### k8s.pods

Get pods from k8s.

#### k8s.execute

Execute command inside k8s pod.

Settings:

* `default_component` default component (Default: `backend`)
* `default_entry` default entry cmd (Default: `/cnb/lifecycle/launcher bash`)

#### k8s.python-shell

Enter python shell inside k8s pod.

Settings:

* `default_component` default component (Default: `backend`)
* `python_shell` shell cmd (Default: `shell_plus`)

#### k8s.health-check

Check health of component.

Settings:

* `default_component` default component (Default: `backend`)
* `health_check` health check cmd (Default: `health_check`)

#### k8s.download-file

Download file from pod.

* `default_component` default component (Default: `backend`)

### db-k8s

While you probably won't use this module directly some other modules
commands are use it(getting remote db dump)

Make sure to set up these configs:

* `pod_namespace` db namespace (**REQUIRED**)
* `pod_selector` pod selector for db (**REQUIRED**)

#### db-k8s.create-dump

Execute dump command in db pod.

Settings:

* `pod_namespace` db namespace (**REQUIRED**)
* `pod_selector` pod selector for db (**REQUIRED**)
* `get_pod_name_command` template for fetching db pod (Default located in `_config.pp > K8SdbSettings`)
* `dump_filename` default dump filename (Default: Name of project from `project_name` plus `_db_dump`)
* `dump_command` dump command template (Default located in `_config.pp > K8SDBSettings`)
* `dump_additional_params` additional dump commands (Default: `--no-owner`)

#### db-k8s.get-dump

Download db data from db pod if it present

Settings:

* `pod_namespace` db namespace (**REQUIRED**)
* `pod_selector` pod selector for db (**REQUIRED**)
* `get_pod_name_command` template for fetching db pod (Default located in `_config.pp > K8SDBSettings`)
* `dump_filename` default dump filename (Default: Name of project from `project_name` plus `_db_dump`)

### cruft

[Cruft](https://cruft.github.io/cruft/) is a tool used to synchronize changes
with cookiecutter based boilerplates.

#### cruft.check-for-cruft-files

Check that there are no cruft files (`*.rej`).

#### cruft.create_project

**Not invocation**, but a shortcut for creating cruft projects for testing
boilerplates

### poetry

#### poetry.install

Install dependencies via poetry.

#### poetry.update

Update dependencies with respect to
[version constraints](https://python-poetry.org/docs/dependency-specification/)
using [poetry up plugin](https://github.com/MousaZeidBaker/poetry-plugin-up).

#### poetry.update-to-latest

Update dependencies to latest versions using
[poetry up plugin](https://github.com/MousaZeidBaker/poetry-plugin-up).

### pip

#### pip.install-dependencies

Install dependencies via pip.

Settings:

* `dependencies_folder` path to folder with dependencies files (Default: `requirements`)

#### pip.compile-dependencies

Compile dependencies via
[pip-compile](https://github.com/jazzband/pip-tools#requirements-from-requirementsin).

Settings:

* `dependencies_folder` path to folder with dependencies files (Default: `requirements`)
* `in_files` sequence of `.in` files (Default: `"production.in"`, `"development.in"`)

### mypy

#### mypy.run

Run mypy in `path` with `params`.

Settings:

* `mypy_entry` python entry command (Default: `-m mypy`)

### pytest

#### pytest.run

Run pytest in `path` with `params`.

Settings:

* `pytest_entry` python entry command (Default: `-m pytest`)
