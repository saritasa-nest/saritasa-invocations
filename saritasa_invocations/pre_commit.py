import invoke

from . import _config, printing


@invoke.task
def install(context: invoke.Context) -> None:
    """Install git hooks via pre-commit."""
    printing.print_success("Setting up pre-commit")
    config: _config.Config = context.config.get(
        "saritasa_invocations",
        _config.Config(),
    )
    hooks = " ".join(f"--hook-type {hook}" for hook in config.pre_commit_hooks)
    context.run(f"pre-commit install {hooks}")


@invoke.task
def run_hooks(context: invoke.Context) -> None:
    """Run all hooks against all files."""
    printing.print_success("Running git hooks")
    context.run("pre-commit run --hook-stage push --all-files")
