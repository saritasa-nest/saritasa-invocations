import invoke

from . import printing


@invoke.task
def install(context: invoke.Context) -> None:
    """Install git hooks via pre-commit."""
    printing.print_success("Setting up pre-commit")
    hooks = " ".join(
        f"--hook-type {hook}"
        for hook in context.config.get("saritasa_invocations", {}).get(
            "pre_commit_hooks",
            (
                "pre-commit",
                "pre-push",
                "commit-msg",
            ),
        )
    )
    context.run(f"pre-commit install {hooks}")


@invoke.task
def run_hooks(context: invoke.Context) -> None:
    """Run all hooks against all files."""
    printing.print_success("Running git hooks")
    context.run("pre-commit run --hook-stage push --all-files")
