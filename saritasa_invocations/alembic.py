import pathlib
import time

import invoke

from . import _config, db, db_k8s, docker, k8s, printing, python


@invoke.task
def wait_for_database(context: invoke.Context) -> None:
    """Ensure that database is up and ready to accept connections.

    Function called just once during subsequent calls of alembic commands.

    """
    if hasattr(wait_for_database, "_called"):
        return
    docker.up(context)
    printing.print_success("Wait for database connection")
    config = _config.Config.from_context(context)
    with _config.context_override(
        context,
        run={
            "echo": False,
            "hide": "out",
        },
    ) as context:
        for _ in range(config.alembic.connect_attempts - 1):
            try:
                # Doing it manually to avoid loop
                python.run(
                    context,
                    command=f"{config.alembic.command} current",
                )
                wait_for_database._called = True  # type: ignore
                return
            except invoke.UnexpectedExit:  # noqa: PERF203
                time.sleep(1)
                continue

    with _config.context_override(
        context,
        run={
            "echo": True,
            "hide": None,
        },
    ) as context:
        try:
            # Do it one more time but without hiding the terminal output
            python.run(
                context,
                command=f"{config.alembic.command} current",
            )
            wait_for_database._called = True  # type: ignore
        except invoke.UnexpectedExit as error:
            printing.print_error(
                "Failed to connect to db, "
                f"after {config.alembic.connect_attempts} attempts",
            )
            raise invoke.Exit(code=1) from error


@invoke.task
def run(context: invoke.Context, command: str) -> None:
    """Execute alembic command."""
    wait_for_database(context)
    config = _config.Config.from_context(context)
    python.run(
        context,
        command=f"{config.alembic.command} {command}",
    )


@invoke.task
def autogenerate(
    context: invoke.Context,
    message: str = "",
) -> None:
    """Autogenerate new version with `message` title.

    Similar to the `manage.py makemigration` command in Django. But you always
    have to check generated versions before upgrade and fix it manually
    if it's necessary.

    """
    if not message:
        raise invoke.Exit(
            code=1,
            message=(
                'Please, use `-m "Version message"` to set message '
                "for autogenerated version."
            ),
        )
    printing.print_success("Autogenerate migrations")
    config = _config.Config.from_context(context)
    rev_id = str(
        len(_get_migration_files_paths(config.alembic.migrations_folder)) + 1,
    )
    rev_id = rev_id.rjust(4, "0")
    command = (
        f'revision --autogenerate --message "{message}" --rev-id={rev_id}'
    )
    run(context, command=command)
    printing.print_success(
        "Migrations generated, please verify them and remove alembic messages",
    )


@invoke.task
def upgrade(
    context: invoke.Context,
    version: str = "head",
) -> None:
    """Upgrade database.

    Use `-v version` to upgrade to the passed version.

    Similar to the `manage.py migrate` command in Django. By default upgrade to
    the `head` - the latest version.

    """
    printing.print_success(f"Migrating to version {version}")
    run(context, command=f"upgrade {version}")


@invoke.task
def downgrade(
    context: invoke.Context,
    version: str = "base",
) -> None:
    """Downgrade database.

    Use `-v version` to downgrade to the passed version.

    Similar to the `manage.py migrate` command in Django. By default downgrade
    to `base` (similar to `migrate zero`).

    """
    printing.print_success(f"Migrating to version {version}")
    run(context, command=f"downgrade {version}")


@invoke.task
def check_for_migrations(
    context: invoke.Context,
) -> None:
    """Check if new migration can be generated."""
    printing.print_success("Checking for migration")
    run(context, command="check")


@invoke.task
def check_for_adjust_messages(
    context: invoke.Context,
) -> None:
    """Check migration files for adjust messages."""
    printing.print_success("Checking migration files for adjust messages")
    config = _config.Config.from_context(context)
    files_to_clean = []
    for filepath in _get_migration_files_paths(
        config.alembic.migrations_folder,
    ):
        with pathlib.Path(filepath).open() as migration_file:
            file_text = migration_file.read()
            for adjust_message in config.alembic.adjust_messages:
                if adjust_message in file_text:
                    files_to_clean.append(str(filepath))
                    break

    if files_to_clean:
        log_files_msg = "\n\t".join(files_to_clean)
        log_messages = "\n".join(config.alembic.adjust_messages)
        printing.print_error(
            f"Adjust messages found in this migration files:\n"
            f"\t{log_files_msg}\n"
            "Ensure that these files does not contain following:\n"
            f"{log_messages}",
        )
        raise invoke.Exit(code=1)


def _get_migration_files_paths(
    migrations_folder: str,
) -> tuple[pathlib.Path, ...]:
    """Get paths of migration files."""
    return tuple(
        path
        for path in pathlib.Path(migrations_folder).glob("*.py")
        if path.name not in ("__init__.py",)
    )


@invoke.task
def load_db_dump(
    context: invoke.Context,
    file: str = "",
    env_file_path: str = ".env",
    reset_db: bool = True,
) -> None:
    """Reset db and load db dump."""
    if reset_db:
        downgrade(context)
    db.load_db_dump(
        context,
        file=file,
        **_load_local_env_db_settings(context, file=env_file_path),
    )


@invoke.task
def backup_local_db(
    context: invoke.Context,
    file: str = "",
    env_file_path: str = ".env",
) -> None:
    """Back up local db."""
    db.backup_local_db(
        context,
        file=file,
        **_load_local_env_db_settings(context, file=env_file_path),
    )


@invoke.task
def backup_remote_db(
    context: invoke.Context,
    file: str = "",
    add_date_to_generated_filename: bool = False,
) -> str:
    """Make dump of remote db and download it."""
    settings = _load_remote_env_db_settings(context)
    db_k8s.create_dump(
        context,
        file=file,
        add_date_to_generated_filename=add_date_to_generated_filename,
        **settings,
    )
    return db_k8s.get_dump(
        context,
        file=file,
        add_date_to_generated_filename=add_date_to_generated_filename,
    )


@invoke.task
def load_remote_db(
    context: invoke.Context,
    file: str = "",
) -> None:
    """Make dump of remote db, download it and apply it."""
    file = backup_remote_db(context, file=file)
    load_db_dump(context, file=file)


def _load_local_env_db_settings(
    context: invoke.Context,
    file: str,
) -> dict[str, str]:
    """Load local db settings from .env file.

    Requires python-decouple:
        https://github.com/HBNetwork/python-decouple

    """
    # decouple could not be installed during project init
    # so we import decouple this way to avoid import errors
    # during project initialization
    import decouple

    secrets = decouple.Config(decouple.RepositoryEnv(file))
    config = _config.Config.from_context(context)
    return {
        arg: str(secrets(env_var))
        for arg, env_var in config.alembic.db_config_mapping.items()
    }


def _load_remote_env_db_settings(
    context: invoke.Context,
) -> dict[str, str]:
    """Load remote db settings from .env file.

    Requires python-decouple:
        https://github.com/HBNetwork/python-decouple

    """
    # decouple could not be installed during project init
    # so we import decouple this way to avoid import errors
    # during project initialization
    import decouple

    with k8s.get_env_secrets(context) as file_path:
        secrets = decouple.Config(decouple.RepositoryEnv(file_path))
        config = _config.Config.from_context(context)
        return {
            arg: str(secrets(env_var))
            for arg, env_var in config.alembic.db_config_mapping.items()
        }
