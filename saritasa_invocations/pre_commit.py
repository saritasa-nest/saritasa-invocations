import os

import invoke

from . import printing


@invoke.task
def install(
    context: invoke.Context,
    hooks: list[str] | None = None,
) -> None:
    """Install git hooks via pre-commit."""
    printing.print_success("Installing pre-commit hooks")
    hooks_str = (
        " ".join(f"--hook-type {hook}" for hook in hooks) if hooks else ""
    )
    context.run(f"pre-commit install {hooks_str}")


@invoke.task
def uninstall(
    context: invoke.Context,
    hooks: list[str] | None = None,
) -> None:
    """Uninstall git hooks via pre-commit."""
    printing.print_success("Uninstalling pre-commit hooks")
    hooks_str = (
        " ".join(f"--hook-type {hook}" for hook in hooks) if hooks else ""
    )
    context.run(f"pre-commit uninstall {hooks_str}")


@invoke.task
def run_hooks(
    context: invoke.Context,
    hook_stage: str = "push",
    params: str = "",
    skip: str = "",
) -> None:
    """Run all hooks against all files."""
    printing.print_success("Running pre-commit hooks")
    context.run(
        f"pre-commit run --hook-stage {hook_stage} --all-files {params}",
        env={
            "SKIP": skip or os.environ.get("SKIP", ""),
        },
    )


@invoke.task
def update(context: invoke.Context) -> None:
    """Update pre-commit dependencies."""
    printing.print_success("Updating pre-commit")
    context.run("pre-commit autoupdate")
