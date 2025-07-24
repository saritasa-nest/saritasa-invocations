import invoke

from . import _config, printing


@invoke.task
def load_db_dump(
    context: invoke.Context,
    dbname: str,
    host: str,
    port: str,
    username: str,
    password: str,
    file: str = "",
    additional_params: str = "",
) -> None:
    """Load db dump to local db."""
    config = _config.Config.from_context(context)
    context.run(
        config.db.load_dump_command.format(
            dbname=dbname,
            host=host,
            port=port,
            username=username,
            file=file or config.db.dump_filename,
            additional_params=additional_params
            or config.db.load_additional_params,
        ),
        watchers=(
            invoke.Responder(
                pattern=config.db.password_pattern,
                response=f"{password}\n",
            ),
        ),
    )
    printing.print_success("DB is ready for use")


@invoke.task
def backup_local_db(
    context: invoke.Context,
    dbname: str,
    host: str,
    port: str,
    username: str,
    password: str,
    file: str = "",
    additional_params: str = "",
) -> None:
    """Back up local db."""
    config = _config.Config.from_context(context)
    printing.print_success("Creating backup of local db.")
    additional_params_list = [
        config.db.dump_additional_params,
    ]
    if config.db.dump_no_owner:
        additional_params_list.append(
            "--no-owner",
        )
    if config.db.dump_include_table:
        additional_params_list.append(
            f"--table={config.db.dump_include_table}",
        )
    if config.db.dump_exclude_table:
        additional_params_list.append(
            f"--exclude-table={config.db.dump_exclude_table}",
        )
    if config.db.dump_exclude_table_data:
        additional_params_list.append(
            f"--exclude-table-data={config.db.dump_exclude_table_data}",
        )
    if config.db.dump_exclude_extension:
        additional_params_list.append(
            f"--exclude-extension={config.db.dump_exclude_extension}",
        )
    context.run(
        config.db.dump_command.format(
            dbname=dbname,
            host=host,
            port=port,
            username=username,
            file=file or config.db.dump_filename,
            additional_params=additional_params
            or " ".join(additional_params_list),
        ),
        watchers=(
            invoke.Responder(
                pattern=config.db.password_pattern,
                response=f"{password}\n",
            ),
        ),
    )
