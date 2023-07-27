import invoke

from . import docker, printing, python


@invoke.task
def run(context) -> None:
    """Run development web-server via FastAPI."""
    docker.up(context)
    printing.print_success("Running web app")
    config = context.config.get("saritasa_invocations", {})
    docker_params = config.get("fastapi_docker_params", "--rm --service-ports")

    uvicorn_command = config.get("fastapi_uvicorn_command", "-m uvicorn")
    app = config.get("fastapi_app", "config:fastapi_app")
    host = config.get("fastapi_host", "0.0.0.0")
    port = config.get("fastapi_port", "8000")
    params = config.get("fastapi_params", "--reload")

    command = f"{uvicorn_command} {app} --host {host} --port {port} {params}"
    python.run(
        context,
        docker_params=docker_params,
        command=command,
    )
