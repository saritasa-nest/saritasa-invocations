import invoke

from . import _config, printing


def get_current_env_config_from_context(
    context: invoke.Context,
) -> _config.K8SSettings:
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

    for env in _config._K8S_CONFIGS.values():
        if (
            env.cluster == current_cluster
            and current_namespace in env.namespace
        ):
            return env

    raise invoke.Exit(
        code=1,
        message=(
            f"Environment data class for the cluster `{current_cluster}`"
            f" and namespace `{current_namespace}` doesn't exits."
        ),
    )


def get_environment(
    context: invoke.Context,
    env_name: str,
) -> _config.K8SSettings:
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
    return environment


def get_pod_cmd(
    context: invoke.Context,
    component: str,
) -> str:
    """Get command for getting exact pod."""
    config = get_current_env_config_from_context(context)
    return (
        "kubectl get pods"
        f" --selector {config.pod_label}={component}"
        " --no-headers --output jsonpath='{.items[0].metadata.name}'"
    )


@invoke.task
def set_context(context: invoke.Context, env: str = "") -> None:
    """Set k8s context to current project."""
    printing.print_success("Setting context for k8s")
    config = _config.Config.from_context(context)
    env = env or config.default_k8s_env
    environment = get_environment(context, env)
    context.run(f"kubectl config use-context {environment.cluster}")
    context.run(
        f"kubectl config set-context"
        f" --current --namespace={environment.namespace}",
    )
    printing.print_success(
        f"`{environment.name}` environment has been set up successfully.",
    )


@invoke.task
def login(context: invoke.Context) -> None:
    """Login into k8s via teleport."""
    printing.print_success("Login into kubernetes CI")
    config = get_current_env_config_from_context(context)
    context.run(
        "tsh login"
        f" --proxy={config.proxy}"
        f" --auth={config.auth}"
        f" --kube-cluster={config.proxy}",
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
def pods(context) -> None:
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
    pod_command: str,
    path_to_file_in_pod: str,
    path_to_where_save_file: str,
    retries: int = -1,
) -> None:
    """Download file from pod."""
    context.run(
        "kubectl cp"
        f" --namespace {pod_namespace}"
        f" --retries={retries}"
        f" $({pod_command}):{path_to_file_in_pod}"
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
        pod_command=get_pod_cmd(
            context,
            component or config.default_component,
        ),
        path_to_file_in_pod=path_to_file_in_pod,
        path_to_where_save_file=path_to_where_save_file,
    )


def success(
    context: invoke.Context,
    message: str,
    env: _config.K8SSettings | None = None,
) -> None:
    """Display success message with mention of environment."""
    if not env:
        env = get_current_env_config_from_context(context)

    printing.print_success(
        message,
        title=f"[{env.env_color} bold underline]{env.name.upper()}",
    )
