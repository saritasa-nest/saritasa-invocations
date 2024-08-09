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
) -> None:
    """Update dependencies with respect to version constraints using poetry up.

    https://python-poetry.org/docs/dependency-specification/

    Fallbacks to `poetry update` in case of an error.

    Requires:
    https://github.com/MousaZeidBaker/poetry-plugin-up

    """
    printing.print_success("Update dependencies")
    try:
        context.run(f"poetry up {params} {_parse_groups(groups)}")
    except invoke.UnexpectedExit:
        printing.print_warn(
            "Can't update with respect to version constraints using poetry up,"
            " trying with poetry update",
        )
        context.run(f"poetry update {_parse_groups(groups)}")


@invoke.task
def update_to_latest(
    context: invoke.Context,
    groups: str = "",
    params: str = "",
    fallback: bool = True,
) -> None:
    """Update dependencies to latest versions using poetry up plugin.

    By default fallbacks to `update` task in case of an error.

    Requires:
    https://github.com/MousaZeidBaker/poetry-plugin-up

    """
    printing.print_success("Update dependencies to latest versions")
    try:
        context.run(f"poetry up --latest {params} {_parse_groups(groups)}")
    except invoke.UnexpectedExit:
        if not fallback:
            raise
        printing.print_warn(
            "Can't update to latest, try to update with respect to version"
            " constraints.",
        )
        update(context, groups=groups, params=params)


def _parse_groups(groups: str) -> str:
    """Parse groups for poetry up."""
    group_arg = " --only "
    group = f"{group_arg}{group_arg.join(groups.split(','))}"

    if group == group_arg:
        return ""

    return group
