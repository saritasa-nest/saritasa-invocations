import os

import invoke

from . import _config, printing


def run_pre_commit_cmd(context: invoke.Context, cmd: str, **kwargs) -> None:
    """Run a pre-commit command."""
    config = _config.Config.from_context(context)
    context.run(command=f"{config.pre_commit.entry} {cmd}", **kwargs)


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
    run_pre_commit_cmd(context=context, cmd=f"install {hooks_str}")


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
    run_pre_commit_cmd(context=context, cmd=f"uninstall {hooks_str}")


@invoke.task
def run_hooks(
    context: invoke.Context,
    hook_stage: str = "",
    params: str = "",
    skip: str = "",
) -> None:
    """Run all hooks against all files."""
    printing.print_success("Running pre-commit hooks")
    config = _config.Config.from_context(context)

    if not hook_stage:
        hook_stage = config.pre_commit.default_hook_stage

    run_pre_commit_cmd(
        context=context,
        cmd=f"run --hook-stage {hook_stage} --all-files {params}",
        env={
            "SKIP": skip or os.environ.get("SKIP", ""),
        },
    )


@invoke.task
def update(context: invoke.Context) -> None:
    """Update pre-commit dependencies."""
    printing.print_success("Updating pre-commit")
    run_pre_commit_cmd(context=context, cmd="autoupdate")
