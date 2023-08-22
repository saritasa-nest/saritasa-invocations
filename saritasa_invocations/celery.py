import invoke

from . import _config, docker, python


@invoke.task
def run(
    context: invoke.Context,
    detach: bool = True,
) -> None:
    """Start celery worker."""
    config = _config.Config.from_context(context)
    match python.get_python_env():
        case python.PythonEnv.LOCAL:
            context.run(config.celery.local_cmd)
        case python.PythonEnv.DOCKER:
            docker.up_containers(
                context,
                (config.celery.service_name,),
                detach=detach,
            )
