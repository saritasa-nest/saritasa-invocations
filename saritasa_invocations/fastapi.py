import invoke

from . import _config, docker, printing, python


@invoke.task
def run(context: invoke.Context) -> None:
    """Run development web-server via FastAPI."""
    docker.up(context)
    printing.print_success("Running web app")
    config: _config.Config = context.config.get(
        "saritasa_invocations",
        _config.Config(),
    )
    command_template = (
        "{uvicorn_command} {app} --host {host} --port {port} {params}"
    )
    python.run(
        context,
        docker_params=config.fastapi_docker_params,
        command=command_template.format(
            uvicorn_command=config.fastapi_uvicorn_command,
            app=config.fastapi_app,
            host=config.fastapi_host,
            port=config.fastapi_port,
            params=config.fastapi_params,
        ),
    )
