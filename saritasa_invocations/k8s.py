import collections
import collections.abc
import contextlib
import pathlib
import typing

import invoke

from . import _config, printing


def get_current_env_config_from_context(
    context: invoke.Context,
) -> _config.K8SGeneratedSettings:
    """Return current environment data class based on current cluster."""
    run_result = context.run(
        "kubectl config current-context",
        echo=False,
        hide="out",
    )
    if not run_result:
        raise invoke.Exit(
            code=1,
            message="Unexpected error, make sure to run inv `k8s.set_context`",
        )
    current_cluster = run_result.stdout.splitlines()[0]

    run_result = context.run(
        "kubectl config view --minify | grep namespace | awk '{print $2}'",
        echo=False,
        hide="out",
    )
    if not run_result:
        raise invoke.Exit(
            code=1,
            message="Unexpected error, make sure to run `inv k8s.set_context`",
        )
    current_namespace = run_result.stdout.splitlines()[0]

    found_env: _config.K8SSettings | None = None
    config = _config.Config.from_context(context)
    for env in config.k8s_configs.values():
        if (
            env.cluster == current_cluster
            and current_namespace in env.namespace
        ):
            found_env = env
            break

    if not found_env:
        raise invoke.Exit(
            code=1,
            message=(
                f"Environment data class for the cluster `{current_cluster}`"
                f" and namespace `{current_namespace}` doesn't exits."
            ),
        )
    return _config.K8SGeneratedSettings.merge_settings(
        default=config.k8s_defaults,
        env_settings=found_env,
    )


def get_environment(
    context: invoke.Context,
    env_name: str,
) -> _config.K8SGeneratedSettings:
    """Get environment by its name."""
    config = _config.Config.from_context(context)
    environment = config.k8s_configs.get(env_name)
    if not environment:
        raise invoke.Exit(
            code=1,
            message=(
                f"Data class for `{env_name}` environment not found. "
                "Available environments: "
                f"{', '.join(config.k8s_configs.keys())}"
            ),
        )
    return _config.K8SGeneratedSettings.merge_settings(
        default=config.k8s_defaults,
        env_settings=environment,
    )


def get_pod_cmd(
    context: invoke.Context,
    component: str,
) -> str:
    """Get command for getting exact pod."""
    config = get_current_env_config_from_context(context)
    return config.get_pod_name_command.format(
        component_selector=config.component_selector,
        component=component,
    )


@invoke.task
def set_context(context: invoke.Context, env: str = "") -> None:
    """Set k8s context to current project."""
    printing.print_success("Setting context for k8s")
    config = _config.Config.from_context(context)
    env = env or config.default_k8s_env
    environment = get_environment(context, env)
    try:
        context.run(f"kubectl config use-context {environment.cluster}")
    except invoke.UnexpectedExit:
        printing.print_warn(
            "User in not logged into environment, attempting to login",
        )
        # User needs to login for first time to be able to use env
        login(context, proxy=environment.proxy, auth=environment.auth)
        context.run(f"kubectl config use-context {environment.cluster}")
    context.run(
        f"kubectl config set-context"
        f" --current --namespace={environment.namespace}",
    )
    printing.print_success(
        f"`{environment.name}` environment has been set up successfully.",
    )


@invoke.task
def login(
    context: invoke.Context,
    proxy: str | None = None,
    auth: str | None = None,
) -> None:
    """Login into k8s via teleport."""
    printing.print_success("Login into kubernetes CI")
    if not proxy and not auth:
        config = get_current_env_config_from_context(context)
        proxy = config.proxy
        auth = config.auth
    context.run(
        "tsh login"
        f" --proxy={proxy}"
        f" --auth={auth}"
        f" --kube-cluster={proxy}",
    )


@invoke.task
def logs(
    context: invoke.Context,
    component: str = "",
) -> None:
    """Get logs for k8s pod."""
    config = get_current_env_config_from_context(context)
    component = component or config.default_component
    success(context, f"Getting logs from {component}")
    context.run(
        f"kubectl logs $({get_pod_cmd(context, component=component)})",
    )


@invoke.task
def pods(
    context: invoke.Context,
) -> None:
    """Get pods from k8s."""
    success(context, "Getting pods")
    context.run("kubectl get pods")


@invoke.task
def execute(
    context: invoke.Context,
    entry: str = "",
    component: str = "",
    pty: bool | None = None,
    hide: str | None = None,
) -> invoke.Result | None:
    """Execute command inside k8s pod."""
    config = get_current_env_config_from_context(context)
    component = component or config.default_component
    entry = entry or config.default_entry
    success(context, f"Entering into {component} with {entry}")
    return context.run(
        f"kubectl exec -ti $({get_pod_cmd(context, component)}) -- {entry}",
        pty=pty,
        hide=hide,
    )


@invoke.task
def python_shell(
    context: invoke.Context,
    component: str = "",
) -> None:
    """Enter into python shell."""
    config = get_current_env_config_from_context(context)
    execute(context, component=component, entry=config.python_shell)


@invoke.task
def health_check(
    context: invoke.Context,
    component: str = "",
) -> None:
    """Check health of component."""
    config = get_current_env_config_from_context(context)
    execute(context, component=component, entry=config.health_check)


def download_file_from_pod(
    context: invoke.Context,
    pod_namespace: str,
    get_pod_name_command: str,
    path_to_file_in_pod: str,
    path_to_where_save_file: str,
    retries: int = -1,
) -> None:
    """Download file from pod."""
    context.run(
        "kubectl cp"
        f" --namespace {pod_namespace}"
        f" --retries={retries}"
        f" $({get_pod_name_command}):{path_to_file_in_pod}"
        f" {path_to_where_save_file}",
    )


@invoke.task
def download_file(
    context: invoke.Context,
    path_to_file_in_pod: str,
    path_to_where_save_file: str,
    component: str = "",
) -> None:
    """Download file from pod."""
    config = get_current_env_config_from_context(context)
    download_file_from_pod(
        context,
        pod_namespace=config.namespace,
        get_pod_name_command=get_pod_cmd(
            context,
            component or config.default_component,
        ),
        path_to_file_in_pod=path_to_file_in_pod,
        path_to_where_save_file=path_to_where_save_file,
    )


@contextlib.contextmanager
def download_file_and_remove_afterwards(
    context: invoke.Context,
    path_to_file_in_pod: str,
    path_to_where_save_file: str,
) -> collections.abc.Generator[str, typing.Any, None]:
    """Download file from k8s and delete it after work is done."""
    download_file(
        context,
        path_to_file_in_pod=path_to_file_in_pod,
        path_to_where_save_file=path_to_where_save_file,
    )
    try:
        yield path_to_where_save_file
    finally:
        printing.print_success(
            f"Deleting file({path_to_where_save_file}) after use",
        )
        pathlib.Path(path_to_where_save_file).unlink()


@contextlib.contextmanager
def get_env_secrets(
    context: invoke.Context,
) -> collections.abc.Generator[str, typing.Any, None]:
    """Get secrets from k8s and save it to file."""
    config = get_current_env_config_from_context(context)
    with download_file_and_remove_afterwards(
        context,
        path_to_file_in_pod=config.secret_file_path_in_pod,
        path_to_where_save_file=config.temp_secret_file_path,
    ) as file_path:
        yield file_path


def success(
    context: invoke.Context,
    message: str,
) -> None:
    """Display success message with mention of environment."""
    env = get_current_env_config_from_context(context)
    printing.print_success(
        message,
        title=f"[{env.env_color} bold underline]{env.name.upper()}",
    )
