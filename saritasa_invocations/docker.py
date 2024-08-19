import collections.abc
import pathlib
import shutil

import invoke

from . import _config, printing


@invoke.task
def build_service(context: invoke.Context, service: str) -> None:
    """Build service image."""
    printing.print_success(f"Building {service}")
    compose_cmd = _config.Config.from_context(context).docker.compose_cmd
    context.run(f"{compose_cmd} build {service}")


@invoke.task
def buildpack(
    context: invoke.Context,
    env: str = "development",
    builder: str = "",
    runner: str = "",
    tag: str = "",
) -> None:
    """Build app image using buildpacks."""
    config = _config.Config.from_context(context)
    # Builder needs requirements.txt
    if pathlib.Path(config.docker.buildpack_requirements_path).exists():
        shutil.copy(
            f"{config.docker.buildpack_requirements_path}/{env}.txt",
            "requirements.txt",
        )
    builder = builder or config.docker.buildpack_builder
    runner = runner or config.docker.buildpack_runner
    tag = tag or config.docker.build_image_tag
    context.run(f"pack build --builder={builder} --run-image={runner} {tag}")
    if pathlib.Path(config.docker.buildpack_requirements_path).exists():
        pathlib.Path("requirements.txt").unlink()


def docker_compose_run(
    context: invoke.Context,
    container: str,
    command: str,
    params: str = "",
    watchers: collections.abc.Sequence[invoke.StreamWatcher] = (),
    env: dict[str, str] | None = None,
) -> None:
    """Run ``command`` using docker-compose.

    docker compose run <params> <container> <command>
    Start container and run command in it.

    Used function so lately it can be extended to use different docker-compose
    files.

    Args:
    ----
        context: Invoke context
        params: Configuration params for docker compose
        container: Name of container to start
        command: Command to run in started container
        watchers: Automated responders to command
        env: environmental variables for run

    """
    compose_cmd = _config.Config.from_context(context).docker.compose_cmd
    env_params = " ".join(
        f"--env {env_key}={value}" for env_key, value in (env or {}).items()
    )
    context.run(
        command=(
            f"{compose_cmd} run {params} {env_params} {container} {command}"
        ),
        watchers=watchers,
    )


def docker_compose_exec(
    context: invoke.Context,
    service: str,
    command: str,
) -> None:
    """Run ``exec`` using docker-compose.

    docker compose exec <service> <command>
    Run commands in already running container.

    Used function so lately it can be extended to use different docker-compose
    files.

    Args:
    ----
        context: Invoke context
        service: Name of service to run command in
        command: Command to run in service container

    """
    compose_cmd = _config.Config.from_context(context).docker.compose_cmd
    cmd = f"{compose_cmd} exec {service} {command}"
    context.run(cmd)


@invoke.task
def stop_all_containers(context: invoke.Context) -> None:
    """Shortcut for stopping ALL running docker containers."""
    context.run("docker stop $(docker ps -q)")


def up_containers(
    context: invoke.Context,
    containers: collections.abc.Sequence[str],
    detach: bool = True,
    stop_others: bool = True,
) -> None:
    """Bring up containers and run them.

    Add `d` kwarg to run them in background.

    Args:
    ----
        context: Invoke context
        containers: Name of containers to start
        detach: To run them in background
        stop_others: Stop ALL other containers in case of errors during `up`.
            Usually this happens when containers from other project uses the
            same ports, for example, Postgres and redis.

    Raises:
    ------
        UnexpectedExit: when `up` command wasn't successful

    """
    if containers:
        printing.print_success(f"Bring up {', '.join(containers)} containers")
    else:
        printing.print_success("Bring up all containers")
    containers_str = " ".join(containers)
    detach_str = "-d " if detach else ""
    compose_cmd = _config.Config.from_context(context).docker.compose_cmd
    up_cmd = f"{compose_cmd} up {detach_str} {containers_str}"
    try:
        context.run(up_cmd)
    except invoke.UnexpectedExit:
        if not stop_others:
            raise
        stop_all_containers(context)
        context.run(up_cmd)


def stop_containers(
    context: invoke.Context,
    containers: collections.abc.Sequence[str],
) -> None:
    """Stop containers."""
    printing.print_success(f"Stopping {' '.join(containers)} containers")
    compose_cmd = _config.Config.from_context(context).docker.compose_cmd
    context.run(f"{compose_cmd} stop {' '.join(containers)}")


@invoke.task
def up(context: invoke.Context) -> None:
    """Bring up main containers and start them."""
    config = _config.Config.from_context(context)
    if not any(
        pathlib.Path(compose_file).exists()
        for compose_file in (
            "compose.yaml",
            "compose.yml",
            "docker-compose.yaml",
            "docker-compose.yml",
        )
    ):
        return
    if not config.docker.main_containers:
        return
    up_containers(
        context,
        containers=config.docker.main_containers,
        detach=True,
    )


@invoke.task
def stop(context: invoke.Context) -> None:
    """Stop main containers."""
    config = _config.Config.from_context(context)
    stop_containers(
        context,
        containers=config.docker.main_containers,
    )


@invoke.task
def clear(context: invoke.Context) -> None:
    """Stop and remove all containers defined in docker-compose.

    Also remove images.

    """
    printing.print_success("Clearing docker-compose")
    compose_cmd = _config.Config.from_context(context).docker.compose_cmd
    context.run(f"{compose_cmd} rm -f")
    context.run(f"{compose_cmd} down -v --rmi all --remove-orphans")
