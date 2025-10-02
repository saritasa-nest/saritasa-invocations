# Version history

We follow [Semantic Versions](https://semver.org/).

## Unreleased

- Add commands for `uv`;

## 1.7.0

- Relax version constraint for python to allow 4.0 and newer
- Make settings pulling for django remote db dumps case insensitive
- Add support for database urls in django remote db dumps invocations

## 1.6.0

- Fix default `docker_service` for `PythonSettings`
- Run celery docker container in foreground by default
- Fix k8s login and adjust `K8SSettings`
  - Now `cluster` is not required while `context` is required
- Rework dump filename generation for `db_k8s`. Now we have `dump_filename_template`
with which you can define template for name. Default: `{project_name}-{env}-{timestamp:%Y-%m-%d}-db-dump.{extension}`. `--add-date-to-generated-filename` option is removed.

## 1.5.0

- Add ability to specify cmd and environment variables for `k8s.execute`
- Improve generated name for k8s db dumps.
Also add `--add-date-to-generated-filename` option to add timestamp for db
dumps from k8s(including commands for django and alembic).
- Add new options for `DBSettings` and `K8SDBSettings`
  - `dump_additional_params` additional params for dump command (Default: ``)
  - `dump_no_owner` add `--no-owner` to dump command (Default: `True`)
  - `dump_include_table` add `--table={dump_include_table}` to dump command (Default: ``)
  - `dump_exclude_table` add `--exclude-table={dump_exclude_table}` to dump command (Default: ``)
  - `dump_exclude_table_data` add `--exclude-table-data={dump_exclude_table_data}` to dump command (Default: ``)
  - `dump_exclude_extension` add `--exclude-extension={dump_exclude_extension}` to dump command (Default: ``)
- Add `builder-env` and `clear-cache` for `docker.buildpack`

## 1.4.0

- Replace `poetry install --sync` to `poetry sync`
- Improve env config extraction for k8s

## 1.3.1

- Fix `git.blame-copy` merging without conflicts

## 1.3.0

- Add params for `system.chown`(`owner` and `path`)
- Add ability to set `dump_dir` for `K8SDBSettings`
- Confirm support for python 3.13

## 1.2.3

- Fix `django.createsuperuser` behavior when git command fails

## 1.2.2

- Make `django.createsuperuser` try to grab username and email from git config

## 1.2.1

- Restore check for main containers in `docker.up`

## 1.2.0

- Replace usage of cmd commands with python
- Make `django.wait_for_database` as task
- Make `alembic.wait_for_database` as task
- Make `docker.up` check for compose file
- Make `pytest.run`, `celery.run` use `docker.up`
- Make sure that `DJANGO_SETTINGS_MODULE` is set for manage invocations

## 1.1.1

- Make default for `default_entry` for `K8SDefaultSettings` use absolute path
according to [specs](https://github.com/buildpacks/spec/blob/main/platform.md#launch)

## 1.1.0

- Fix `git.blame-copy` in case if merge conflict between files occurs.
- Made pip commands shorter:
  - `inv pip.install-dependencies` -> `inv pip.install`;
  - `inv pip.compile-dependencies` -> `inv pip.compile`;
  - From now `pip.install-dependencies` and  `pip.compile-dependencies` are
    deprecated commands. They will be removed in next releases.
- Add `branch`, `clone_params`, `pull_params`, `checkout_params` parameter to `git.clone-repo` invocation

## 1.0.0

First stable release

## 0.10.1

- Add `__all__` to `__init__`.py.
Without it in VS Code, `Pylance` will raise `reportPrivateImportUsage` when trying to import non-module names from package.

## 0.10.0

- Add configuration for django `manage.py` file path
- Improve `pre-commit.run-hooks` command with `params`
- Add `git.blame-copy` command
- Add fallback for `poetry.update` and `poetry.update_to_latest`

## 0.9.1

- Fix celery configuration

## 0.9.0

- Add `django.startapp` invocation.
- Confirm support for python 3.12.
- Add `secrets` invocations
- Extend `alembic` invocations to be able to make db dumps
- Improve logic of `wait_for_database` for `alembic`
- Add invocation for `celery` to run task

## 0.8.3

- Make `context_override` public

## 0.8.2

- Hotfix context override

## 0.8.1

- Add wait logic for alembic run invocations
- Add ignore for `__init__.py` file in migrations folder for alembic invocations
- Add ability to customize pod command template for k8s invocations

## 0.8.0

- Improve `django.createsuperuser` command with verbose name settings
- Fix k8s.set-context when user is not logged in for first time
- Add pip invocations
- Add mypy invocations
- Add pytest invocations

## 0.7.1

- Add `recompile-messages` command to django invocations
- Fix docs for python invocations
- Fix `docker.clear` command

## 0.7.0

- Add default config feature for k8s

## 0.6.2

- Fix default config init

## 0.6.1

- Fix poetry file

## 0.6.0

- Add cruft invocations
- Add poetry invocations
- Add update invocation to pre-commit
- Make docker compose cmd customizable
- Fix k8s errors for multiple app pods

## 0.5.3

- Fix `django.backup_remote_db`

## 0.5.2

- Fix typo in `load_additional_params`
- Improve `password_pattern` for db setting

## 0.5.1

- Fix default db commands templates

## 0.5.0

- Add db invocations
- Add k8s invocations
- Add db_k8s invocations

## 0.4.1

- Add `FastAPISettings` to imports

## 0.4.0

- Rework configuration

## 0.3.0

- Improve readme
- Add alembic invocations

## 0.2.0

- Add python invocations
- Add django invocations
- Add fastapi invocations
- Add celery invocations
- Add open-api invocations

## 0.1.0

- Beta release
