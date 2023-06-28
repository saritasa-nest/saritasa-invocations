import os

import invoke


@invoke.task
def copy_local_settings(
    context: invoke.Context,
    force_update: bool = False,
) -> None:
    """Copy local settings from template.

    Args:
        force_update: rewrite file if exists or not

    """
    config = context.config.get("saritasa_invocations", {})
    _rewrite_file(
        context=context,
        from_path=config.get(
            "settings_template",
            "config/settings/local.template.py",
        ),
        to_path=config.get(
            "save_settings_from_template_to",
            "config/settings/local.py",
        ),
        force_update=force_update,
    )


@invoke.task
def copy_vscode_settings(
    context: invoke.Context,
    force_update=False,
) -> None:
    """Copy vscode settings from template.

    Args:
        force_update: rewrite file if exists or not

    """
    config = context.config.get("saritasa_invocations", {})
    _rewrite_file(
        context=context,
        from_path=config.get(
            "vs_code_settings_template",
            ".vscode/recommended_settings.json",
        ),
        to_path=".vscode/settings.json",
        force_update=force_update,
    )


def _rewrite_file(
    context: invoke.Context,
    from_path: str,
    to_path: str,
    force_update=False,
) -> None:
    """Copy file to destination."""
    if force_update or not os.path.isfile(to_path):
        context.run(" ".join(("cp", from_path, to_path)))


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
    context.run("mkdir -p .tmp")
