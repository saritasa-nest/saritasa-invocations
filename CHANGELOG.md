# Version history

We follow [Semantic Versions](https://semver.org/).

## unreleased

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
