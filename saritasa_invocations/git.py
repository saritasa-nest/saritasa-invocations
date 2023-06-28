import invoke

from . import pre_commit, printing


@invoke.task
def setup(context: invoke.Context) -> None:
    """Set up git for working."""
    printing.print_success("Setting up git and pre-commit")
    pre_commit.install(context)

    config = context.config.get("saritasa_invocations", {})
    merge_ff = config.get("merge_ff", "false")
    set_git_setting(context, setting="merge.ff", value=merge_ff)
    pull_ff = config.get("pull_ff", "only")
    set_git_setting(context, setting="pull.ff", value=pull_ff)


def set_git_setting(
    context: invoke.Context,
    setting: str,
    value: str,
) -> None:
    """Set git setting in config."""
    context.run(f"git config --local --add {setting} {value}")
