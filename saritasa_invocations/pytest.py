import invoke

from . import _config, printing, python


@invoke.task
def run(
    context: invoke.Context,
    path: str = ".",
    params: str = "",
) -> None:
    """Run pytest in `path` with `params`."""
    printing.print_success("Running PyTest")
    pytest_entry = _config.Config.from_context(context).python.pytest_entry
    python.run(context, f"{pytest_entry} {path} {params}")
