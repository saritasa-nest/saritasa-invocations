import invoke

from . import _config, docker, python


@invoke.task
def run(
    context: invoke.Context,
    detach: bool = True,
) -> None:
    """Start celery worker."""
    config = _config.Config.from_context(context).celery
    match python.get_python_env():
        case python.PythonEnv.LOCAL:
            docker.up(context)
            context.run(
                config.local_cmd.format(
                    app=config.app,
                    scheduler=config.scheduler,
                    loglevel=config.loglevel,
                    extra_params=" ".join(config.extra_params),
                ),
            )
        case python.PythonEnv.DOCKER:
            docker.up_containers(
                context,
                (config.service_name,),
                detach=detach,
            )


@invoke.task
def send_task(
    context: invoke.Context,
    task: str,
) -> None:
    """Send task to celery worker."""
    config = _config.Config.from_context(context).celery
    python.run(context, f"-m celery --app {config.app} call {task}")
