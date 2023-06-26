import invoke

from . import printing


@invoke.task
def set_up_hosts(context: invoke.Context) -> None:
    """Add hosts to /etc/hosts."""
    printing.print_success("Setting up hosts")

    config = context.config.get("saritasa_invocations", {})
    hosts = config.get(
        "github_action_hosts",
        config.get(
            "docker_main_containers",
            (
                "postgres",
                "redis",
            ),
        ),
    )
    for host in hosts:
        set_up_host(context, host=host)


def set_up_host(context: invoke.Context, host: str) -> None:
    """Add host to /etc/hosts."""
    context.run(f'echo "127.0.0.1 {host}" | sudo tee -a /etc/hosts')
