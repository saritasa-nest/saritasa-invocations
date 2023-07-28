import invoke

from . import _config, docker, printing, python


@invoke.task
def run(context: invoke.Context) -> None:
    """Run development web-server via FastAPI."""
    docker.up(context)
    printing.print_success("Running web app")
    config = _config.Config.from_context(context)
    command_template = (
        "{uvicorn_command} {app} --host {host} --port {port} {params}"
    )
    python.run(
        context,
        docker_params=config.fastapi.docker_params,
        command=command_template.format(
            uvicorn_command=config.fastapi.uvicorn_command,
            app=config.fastapi.app,
            host=config.fastapi.host,
            port=config.fastapi.port,
            params=config.fastapi.params,
        ),
    )
