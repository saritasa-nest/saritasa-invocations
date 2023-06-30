import invoke

from . import docker, python


@invoke.task
def run(
    context: invoke.Context,
    detach: bool = True,
) -> None:
    """Start celery worker."""
    config = context.config.get("saritasa_invocations", {})
    match python.get_python_env():
        case python.PythonEnv.LOCAL:
            celery_local_cmd = config.get(
                "celery_local_cmd",
                (
                    "celery --app config.celery:app "
                    "worker --beat --scheduler=django --loglevel=info"
                ),
            )
            context.run(celery_local_cmd)
        case python.PythonEnv.DOCKER:
            celery_service_name = config.get(
                "celery_service_name",
                "celery",
            )
            docker.up_containers(
                context,
                (celery_service_name,),
                detach=detach,
            )
