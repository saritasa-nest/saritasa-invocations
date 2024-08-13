import pathlib
import shutil

import invoke

from . import _config


@invoke.task
def copy_local_settings(
    context: invoke.Context,
    force_update: bool = False,
) -> None:
    """Copy local settings from template.

    Args:
    ----
        context: invoke's context
        force_update: rewrite file if exists or not

    """
    config = _config.Config.from_context(context)
    _rewrite_file(
        context=context,
        from_path=config.system.settings_template,
        to_path=config.system.save_settings_from_template_to,
        force_update=force_update,
    )


@invoke.task
def copy_vscode_settings(
    context: invoke.Context,
    force_update: bool = False,
) -> None:
    """Copy vscode settings from template.

    Args:
    ----
        context: invoke's context
        force_update: rewrite file if exists or not

    """
    config = _config.Config.from_context(context)
    _rewrite_file(
        context=context,
        from_path=config.system.vs_code_settings_template,
        to_path=".vscode/settings.json",
        force_update=force_update,
    )


def _rewrite_file(
    context: invoke.Context,
    from_path: str,
    to_path: str,
    force_update: bool = False,
) -> None:
    """Copy file to destination."""
    if force_update or not pathlib.Path(to_path).is_file():
        shutil.copy(from_path, to_path)


@invoke.task
def chown(context: invoke.Context) -> None:
    """Change owner ship of project files to current user.

    Shortcut for owning apps dir by current user after some files were
    generated using docker-compose (migrations, new app, etc).

    """
    context.run("sudo chown -R ${USER}: .")


@invoke.task
def create_tmp_folder(context: invoke.Context) -> None:
    """Create folder for temporary files."""
    pathlib.Path(".tmp").mkdir(parents=True, exist_ok=True)
