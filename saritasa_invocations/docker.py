import os
import typing

import invoke

from . import printing


@invoke.task
def build_service(context: invoke.Context, service) -> None:
    """Build service image."""
    printing.print_success(f"Building {service}")
    context.run(f"docker-compose build {service}")


@invoke.task
def buildpack(
    context: invoke.Context,
    env: str = "development",
    builder: str = "",
    runner: str = "",
    tag: str = "",
) -> None:
    """Build app image using buildpacks."""
    config = context.config.get("saritasa_invocations", {})
    builder = builder or config.get(
        "buildpack_builder",
        "paketobuildpacks/builder:base",
    )
    runner = runner or config.get(
        "buildpack_runner",
        "paketobuildpacks/run:base",
    )
    tag = tag or config.get("build_image_tag") or config.get("project_name")
    buildpack_requirements_path = config.get(
        "buildpack_requirements_path",
        "requirements",
    )
    # Builder needs requirements.txt
    if buildpack_requirements_path and os.path.exists(
        buildpack_requirements_path,
    ):
        context.run(
            f"cp {buildpack_requirements_path}/{env}.txt requirements.txt",
        )
    context.run(f"pack build --builder={builder} --run-image={runner} {tag}")
    if buildpack_requirements_path and os.path.exists(
        buildpack_requirements_path,
    ):
        context.run("rm requirements.txt")


def docker_compose_run(
    context: invoke.Context,
    params: str | None,
    container: str,
    command: str,
    watchers: typing.Iterable[invoke.StreamWatcher] = (),
) -> None:
    """Run ``command`` using docker-compose.

    docker-compose run <params> <container> <command>
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
    context.run(
        command=f"docker-compose run {params or ''} {container} {command}",
        watchers=watchers,
    )


def docker_compose_exec(
    context: invoke.Context,
    service: str,
    command: str,
) -> None:
    """Run ``exec`` using docker-compose.

    docker-compose exec <service> <command>
    Run commands in already running container.

    Used function so lately it can be extended to use different docker-compose
    files.

    Args:
        context: Invoke context
        service: Name of service to run command in
        command: Command to run in service container

    """
    cmd = f"docker-compose exec {service} {command}"
    context.run(cmd)


@invoke.task
def stop_all_containers(context: invoke.Context) -> None:
    """Shortcut for stopping ALL running docker containers."""
    context.run("docker stop $(docker ps -q)")


def up_containers(
    context: invoke.Context,
    containers: typing.Iterable[str],
    detach: bool = True,
    stop_others: bool = True,
    **kwargs,
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
    up_cmd = f"docker-compose up {detach_str} {containers_str}"
    try:
        context.run(up_cmd)
    except invoke.UnexpectedExit as exception:
        if not stop_others:
            raise exception
        stop_all_containers(context)
        context.run(up_cmd)


def stop_containers(
    context: invoke.Context,
    containers: typing.Iterable[str],
) -> None:
    """Stop containers."""
    printing.print_success(f"Stopping {' '.join(containers)} containers")
    context.run(f"docker-compose stop {' '.join(containers)}")


@invoke.task
def up(context: invoke.Context) -> None:
    """Bring up main containers and start them."""
    config = context.config.get("saritasa_invocations", {})
    up_containers(
        context,
        containers=config.get(
            "docker_main_containers",
            (
                "postgres",
                "redis",
            ),
        ),
        detach=True,
    )


@invoke.task
def stop(context: invoke.Context) -> None:
    """Stop main containers."""
    config = context.config.get("saritasa_invocations", {})
    stop_containers(
        context,
        containers=config.get(
            "docker_main_containers",
            (
                "postgres",
                "redis",
            ),
        ),
    )


@invoke.task
def clear(context: invoke.Context) -> None:
    """Stop and remove all containers defined in docker-compose.

    Also remove images.

    """
    printing.print_success("Clearing docker-compose")
    context.run("docker-compose rm -f")
    context.run("docker-compose down -v --rmi all --remove-orphans")
