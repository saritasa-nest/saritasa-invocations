import invoke

from . import _config, printing


@invoke.task
def install_dependencies(
    context: invoke.Context,
    env: str = "development",
) -> None:
    """Install dependencies via pip."""
    printing.print_success(f"Install dependencies with pip from {env}.txt")
    config = _config.Config.from_context(context)
    context.run(f"pip install -r {config.pip.dependencies_folder}/{env}.txt")


@invoke.task
def compile_dependencies(
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
