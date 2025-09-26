import invoke

from . import printing


@invoke.task
def sync(
    context: invoke.Context,
    params: str = "--all-groups --locked",
) -> None:
    """Install dependencies via uv."""
    printing.print_success("Install dependencies with uv")
    context.run(f"uv sync {params}")


@invoke.task
def update(
    context: invoke.Context,
    params: str = "",
) -> None:
    """Update dependencies with respect to version constraints using uv.

    uv doesn't have command to upgrade package versions and
    change pyproject.toml.
    See this https://github.com/astral-sh/uv/issues/1419#issuecomment-2849420114
    from maintainer (1st and 2nd points).

    """
    printing.print_success("Update dependencies")
    context.run(f"uv lock --upgrade {params}")
