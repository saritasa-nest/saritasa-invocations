import invoke

from . import _config, pre_commit, printing


@invoke.task
def setup(context: invoke.Context) -> None:
    """Set up git for working."""
    printing.print_success("Setting up git and pre-commit")
    pre_commit.install(context)

    config: _config.Config = context.config.get(
        "saritasa_invocations",
        _config.Config(),
    )
    set_git_setting(
        context,
        setting="merge.ff",
        value=config.merge_ff,
    )
    set_git_setting(
        context,
        setting="pull.ff",
        value=config.pull_ff,
    )


def set_git_setting(
    context: invoke.Context,
    setting: str,
    value: str,
) -> None:
    """Set git setting in config."""
    context.run(f"git config --local --add {setting} {value}")
