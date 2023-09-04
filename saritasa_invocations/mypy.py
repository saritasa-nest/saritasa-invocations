import invoke

from . import _config, printing, python


@invoke.task
def run(
    context: invoke.Context,
    path: str = ".",
    params: str = "",
) -> None:
    """Run mypy in `path` with `params`."""
    printing.print_success("Running MyPy")
    mypy_entry = _config.Config.from_context(context).python.mypy_entry
    python.run(context, command=f"{mypy_entry} {path} {params}")
