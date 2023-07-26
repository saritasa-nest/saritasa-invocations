import enum
import os
import typing

import invoke

from . import docker


class StrEnum(str, enum.Enum):
    """Support python 3.10."""


class PythonEnv(StrEnum):
    """All possible python environments."""

    DOCKER = "docker"
    LOCAL = "local"


def get_python_env() -> PythonEnv:
    """Get python environment."""
    python_env = os.environ.get("PYTHON_ENV", PythonEnv.LOCAL.value).lower()
    supported_envs = tuple(PythonEnv)
    if python_env not in supported_envs:
        raise invoke.Exit(
            code=1,
            message=(
                "Invalid `PYTHON_ENV` variable, "
                f"expected: {', '.join(PythonEnv)}, got {python_env}!"
            ),
        )
    return PythonEnv(python_env)


def run_docker(
    context: invoke.Context,
    command: str,
    params: str | None = None,
    watchers: typing.Iterable[invoke.StreamWatcher] = (),
) -> None:
    """Run command in `python` container."""
    config = context.config.get("saritasa_invocations", {})
    python_docker_service = config.get("python_docker_service", "web")
    if params is None:
        params = config.get("python_docker_service_params", "--rm")
    docker.docker_compose_run(
        context,
        params=params,
        container=python_docker_service,
        command=command,
        watchers=watchers,
    )


def run_docker_python(
    context: invoke.Context,
    command: str,
    params: str | None = None,
    watchers: typing.Iterable[invoke.StreamWatcher] = (),
) -> None:
    """Run command using docker python interpreter."""
    config = context.config.get("saritasa_invocations", {})
    python_entry = config.get("python_entry", "python")
    run_docker(
        context=context,
        params=params,
        command=f"{python_entry} {command}",
        watchers=watchers,
    )


def run_local_python(
    context: invoke.Context,
    command: str,
    watchers: typing.Iterable[invoke.StreamWatcher] = (),
) -> None:
    """Run command using local python interpreter."""
    config = context.config.get("saritasa_invocations", {})
    python_entry = config.get("python_entry", "python")
    context.run(
        command=f"{python_entry} {command}",
        watchers=watchers,
    )


@invoke.task
def run(
    context: invoke.Context,
    command: str,
    docker_params: str | None = None,
    watchers: typing.Iterable[invoke.StreamWatcher] = (),
) -> None:
    """Execute python command."""
    match get_python_env():
        case PythonEnv.LOCAL:
            run_local_python(
                context=context,
                command=command,
                watchers=watchers,
            )
        case PythonEnv.DOCKER:
            run_docker_python(
                context=context,
                command=command,
                params=docker_params,
                watchers=watchers,
            )
