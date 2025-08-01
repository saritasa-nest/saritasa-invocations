import datetime
import pathlib

import invoke

from . import _config, k8s


@invoke.task
def create_dump(
    context: invoke.Context,
    dbname: str,
    host: str,
    port: str,
    username: str,
    password: str,
    file: str = "",
    additional_params: str = "",
) -> None:
    """Execute dump command in db pod."""
    config = _config.Config.from_context(context)
    command = _generate_dump_command(
        context,
        file=file,
        dbname=dbname,
        host=host,
        port=port,
        username=username,
        additional_params=additional_params,
    )
    k8s.success(context, f"Entering into db with {command}")
    db_exec_command = _generate_exec_command(context)
    context.run(
        f"{db_exec_command} -- {command}",
        watchers=(
            invoke.Responder(
                pattern=config.db.password_pattern,
                response=f"{password}\n",
            ),
        ),
    )


@invoke.task
def get_dump(
    context: invoke.Context,
    file: str = "",
) -> str:
    """Download db data from db pod if it present."""
    config = k8s.get_current_env_config_from_context(context).db_config
    file = _get_db_k8s_dump_filename(context)

    k8s.success(context, f"Downloading dump ({file}) from pod")
    dump_path = f"{config.dump_dir}/{file}"
    k8s.download_file_from_pod(
        context,
        pod_namespace=config.namespace,
        get_pod_name_command=_generate_get_pod_name_command(context),
        path_to_file_in_pod=dump_path,
        path_to_where_save_file=f"{pathlib.Path.cwd()}/{file}",
    )
    k8s.success(context, f"Downloaded dump ({file}) from pod. Clean up")
    context.run(f"{_generate_exec_command(context)} -- rm {dump_path}")
    return file


def _generate_get_pod_name_command(context: invoke.Context) -> str:
    """Generate pod command for db."""
    config = k8s.get_current_env_config_from_context(context).db_config
    return config.get_pod_name_command.format(
        db_pod_namespace=config.namespace,
        db_pod_selector=config.pod_selector,
    )


def _generate_exec_command(context: invoke.Context) -> str:
    """Generate exec command for db."""
    config = k8s.get_current_env_config_from_context(context).db_config
    return config.exec_command.format(
        db_pod_namespace=config.namespace,
        db_pod=_generate_get_pod_name_command(context),
    )


def _generate_dump_command(
    context: invoke.Context,
    dbname: str,
    host: str,
    port: str,
    username: str,
    file: str = "",
    additional_params: str = "",
) -> str:
    """Generate for preforming remote dump."""
    config = k8s.get_current_env_config_from_context(context).db_config
    filename = _get_db_k8s_dump_filename(
        context,
        file=file,
    )
    additional_params_list = [
        config.dump_additional_params,
    ]
    if config.dump_no_owner:
        additional_params_list.append(
            "--no-owner",
        )
    if config.dump_include_table:
        additional_params_list.append(
            f"--table={config.dump_include_table}",
        )
    if config.dump_exclude_table:
        additional_params_list.append(
            f"--exclude-table={config.dump_exclude_table}",
        )
    if config.dump_exclude_table_data:
        additional_params_list.append(
            f"--exclude-table-data={config.dump_exclude_table_data}",
        )
    if config.dump_exclude_extension:
        additional_params_list.append(
            f"--exclude-extension={config.dump_exclude_extension}",
        )
    return config.dump_command.format(
        dbname=dbname,
        host=host,
        port=port,
        username=username,
        file=f"{config.dump_dir}/{filename}",
        additional_params=additional_params
        or " ".join(additional_params_list),
    )


def _get_db_k8s_dump_filename(
    context: invoke.Context,
    file: str = "",
) -> str:
    """Get filename for db dump."""
    config = _config.Config.from_context(context)
    k8s_config = k8s.get_current_env_config_from_context(context)
    k8s_db_config = k8s_config.db_config
    generated_filename = k8s_db_config.dump_filename_template.format(
        project_name=config.project_name,
        env=k8s_config.name,
        timestamp=datetime.datetime.now(tz=datetime.timezone.utc),
        extension="sql",
    )
    return file or generated_filename
