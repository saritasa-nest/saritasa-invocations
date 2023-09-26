import collections.abc
import os

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
    if os.path.exists(config.docker.buildpack_requirements_path):
        context.run(
            f"cp {config.docker.buildpack_requirements_path}/{env}.txt "
            "requirements.txt",
        )
    builder = builder or config.docker.buildpack_builder
    runner = runner or config.docker.buildpack_runner
    tag = tag or config.docker.build_image_tag
    context.run(f"pack build --builder={builder} --run-image={runner} {tag}")
    if os.path.exists(config.docker.buildpack_requirements_path):
        context.run("rm requirements.txt")


def docker_compose_run(
    context: invoke.Context,
    params: str | None,
    container: str,
    command: str,
    watchers: collections.abc.Sequence[invoke.StreamWatcher] = (),
) -> None:
    """Run ``command`` using docker-compose.

    docker compose run <params> <container> <command>
    Start container and run command in it.

    Used function so lately it can be extended to use different docker-compose
    files.

    Args:
        context: Invoke context
        params: Configuration params for docker compose
        container: Name of container to start
        command: Command to run in started container
        watchers: Automated responders to command

    """
    compose_cmd = _config.Config.from_context(context).docker.compose_cmd
    context.run(
        command=f"{compose_cmd} run {params or ''} {container} {command}",
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
        context: Invoke context
        containers: Name of containers to start
        detach: To run them in background
        stop_others: Stop ALL other containers in case of errors during `up`.
            Usually this happens when containers from other project uses the
            same ports, for example, Postgres and redis.

    Raises:
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
    except invoke.UnexpectedExit as exception:
        if not stop_others:
            raise exception
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


def pull_images(
    context: invoke.Context,
    services: collections.abc.Sequence[str],
) -> None:
    """Pull docker images to bring up containers."""
    config = _config.Config.from_context(context)
    if services:
        printing.print_success(
            f"Pulling images associated with services {', '.join(services)}",
        )
    else:
        printing.print_success("Pulling all images")
    services_str = " ".join(services)
    compose_cmd = config.docker.compose_cmd
    pull_params = config.docker.pull_params
    pull_cmd = f"{compose_cmd} pull {pull_params} {services_str}"
    context.run(pull_cmd)


@invoke.task
def pull(context: invoke.Context) -> None:
    """Pull images associated with main containers."""
    config = _config.Config.from_context(context)
    if not config.docker.main_containers:
        return
    pull_images(
        context,
        services=config.docker.main_containers,
    )


@invoke.task
def up(context: invoke.Context) -> None:
    """Bring up main containers and start them."""
    config = _config.Config.from_context(context)
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
