import invoke

from . import _config, printing


@invoke.task
def install(context: invoke.Context) -> None:
    """Install git hooks via pre-commit."""
    printing.print_success("Setting up pre-commit")
    config = _config.Config.from_context(context)
    hooks = " ".join(f"--hook-type {hook}" for hook in config.pre_commit.hooks)
    context.run(f"pre-commit install {hooks}")


@invoke.task
def run_hooks(context: invoke.Context, params: str = "") -> None:
    """Run all hooks against all files."""
    printing.print_success("Running git hooks")
    context.run(f"pre-commit run --hook-stage push --all-files {params}")


@invoke.task
def update(context: invoke.Context) -> None:
    """Update pre-commit dependencies."""
    printing.print_success("Updating pre-commit")
    context.run("pre-commit autoupdate")
