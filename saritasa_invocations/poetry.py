import invoke

from . import printing


@invoke.task
def install(context: invoke.Context) -> None:
    """Install dependencies via poetry."""
    printing.print_success("Install dependencies with poetry")
    context.run("poetry install --sync")


@invoke.task
def update(
    context: invoke.Context,
    groups: str = "",
    params: str = "",
):
    """Update dependencies with respect to version constraints using poetry up.

    https://python-poetry.org/docs/dependency-specification/

    Requires:
    https://github.com/MousaZeidBaker/poetry-plugin-up

    """
    printing.print_success("Update dependencies")
    context.run(f"poetry up {params} {_parse_groups(groups)}")


@invoke.task
def update_to_latest(
    context: invoke.Context,
    groups: str = "",
    params: str = "",
):
    """Update dependencies to latest versions using poetry up plugin.

    Requires:
    https://github.com/MousaZeidBaker/poetry-plugin-up

    """
    printing.print_success("Update dependencies to latest versions")
    context.run(f"poetry up --latest {params} {_parse_groups(groups)}")


def _parse_groups(groups: str) -> str:
    """Parse groups for poetry up."""
    group_arg = " --only "
    group = f"{group_arg}{group_arg.join(groups.split(','))}"

    if group == group_arg:
        return ""

    return group
