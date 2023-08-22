import invoke

from . import _config, printing


@invoke.task
def set_up_hosts(context: invoke.Context) -> None:
    """Add hosts to /etc/hosts."""
    printing.print_success("Setting up hosts")

    config = _config.Config.from_context(context)
    for host in config.github_actions.hosts:
        set_up_host(context, host=host)


def set_up_host(context: invoke.Context, host: str) -> None:
    """Add host to /etc/hosts."""
    context.run(f'echo "127.0.0.1 {host}" | sudo tee -a /etc/hosts')
