import invoke

from . import _config, printing


@invoke.task(aliases=["install-dependencies"])
def install(
    context: invoke.Context,
    env: str = "development",
) -> None:
    """Install dependencies via pip."""
    printing.print_success(f"Install dependencies with pip from {env}.txt")
    config = _config.Config.from_context(context)
    context.run(f"pip install -r {config.pip.dependencies_folder}/{env}.txt")


def install_dependencies(
    context: invoke.Context,
    env: str = "development",
) -> None:
    """Install dependencies via pip."""
    printing.print_warn(
        "It is deprecated command. It will be removed in next releases."
        " Use the short version of this command `inv pip.install`.",
    )
    install(context, env)


@invoke.task(aliases=["compile-dependencies"])
def compile(  # noqa: A001
    context: invoke.Context,
    upgrade: bool = False,
) -> None:
    """Compile dependencies via pip-compile.

    Requires:
    https://github.com/jazzband/pip-tools

    """
    printing.print_success("Compile requirements with pip-compile")
    upgrade_param = "-U" if upgrade else ""
    config = _config.Config.from_context(context)
    dependencies_folder = config.pip.dependencies_folder

    for file in config.pip.in_files:
        context.run(
            f"pip-compile -q {dependencies_folder}/{file} {upgrade_param}",
        )


def compile_dependencies(
    context: invoke.Context,
    upgrade: bool = False,
) -> None:
    """Compile dependencies via pip-compile.

    Requires:
    https://github.com/jazzband/pip-tools

    """
    printing.print_warn(
        "It is deprecated command. It will be removed in next releases."
        " Use the short version of this command `inv pip.compile`.",
    )
    compile(context, upgrade)
