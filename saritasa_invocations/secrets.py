import collections.abc
import pathlib
import re

import invoke

from . import k8s


@invoke.task(iterable=["credentials"])
def setup_env_credentials(
    context: invoke.Context,
    credentials: collections.abc.Sequence[str],
    env_file_path: str = ".env",
) -> None:
    """Fill specified credentials.

    Requires python-decouple:
        https://github.com/HBNetwork/python-decouple

    """
    # decouple could not be installed during project init
    # so we import decouple this way to avoid import errors
    # during project initialization

    import decouple

    with k8s.get_env_secrets(context) as file_path:
        secrets = decouple.Config(decouple.RepositoryEnv(file_path))
        cred_params = {cred: str(secrets(cred)) for cred in credentials}
        env_secret_replacer(
            env_file_path=env_file_path,
            **cred_params,
        )


def env_secret_replacer(env_file_path: str, **credentials) -> None:
    """Replace secret in env file."""
    with pathlib.Path(env_file_path).open() as env_file:
        env_data = env_file.read()
    with pathlib.Path(env_file_path).open(mode="w") as env_file:
        for cred, value in credentials.items():
            env_data = re.sub(
                rf"{cred}=.*\n",
                rf"{cred}={value}\n",
                env_data,
                count=1,
            )
        env_file.write(env_data)
