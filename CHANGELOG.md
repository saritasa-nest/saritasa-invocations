# Version history

We follow [Semantic Versions](https://semver.org/).

## unreleased

- Improve `django.createsuperuser` command with verbose name settings
- Fix k8s.set-context when user is not logged in for first time
- Add pip invocations

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
