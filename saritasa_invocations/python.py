import collections.abc
import enum
import os

import invoke

from . import _config, docker


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
    watchers: collections.abc.Sequence[invoke.StreamWatcher] = (),
    env: dict[str, str] | None = None,
) -> None:
    """Run command in `python` container."""
    config = _config.Config.from_context(context)
    if params is None:
        params = config.python.docker_service_params
    docker.docker_compose_run(
        context,
        params=params,
        container=config.python.docker_service,
        command=command,
        watchers=watchers,
        env=env,
    )


def run_docker_python(
    context: invoke.Context,
    command: str,
    params: str | None = None,
    watchers: collections.abc.Sequence[invoke.StreamWatcher] = (),
    env: dict[str, str] | None = None,
) -> None:
    """Run command using docker python interpreter."""
    config = _config.Config.from_context(context)
    run_docker(
        context=context,
        params=params,
        command=f"{config.python.entry} {command}",
        watchers=watchers,
        env=env,
    )


def run_local_python(
    context: invoke.Context,
    command: str,
    watchers: collections.abc.Sequence[invoke.StreamWatcher] = (),
    env: dict[str, str] | None = None,
) -> None:
    """Run command using local python interpreter."""
    config = _config.Config.from_context(context)
    context.run(
        command=f"{config.python.entry} {command}",
        watchers=watchers,
        env=env,
    )


@invoke.task
def run(
    context: invoke.Context,
    command: str,
    docker_params: str | None = None,
    watchers: collections.abc.Sequence[invoke.StreamWatcher] = (),
    env: dict[str, str] | None = None,
) -> None:
    """Execute python command."""
    match get_python_env():
        case PythonEnv.LOCAL:
            run_local_python(
                context=context,
                command=command,
                watchers=watchers,
                env=env,
            )
        case PythonEnv.DOCKER:
            run_docker_python(
                context=context,
                command=command,
                params=docker_params,
                watchers=watchers,
                env=env,
            )
