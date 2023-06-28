# saritasa-invocations

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
            "docker-main-container" = [
                "opensearch",
                "redis",
            ],
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
