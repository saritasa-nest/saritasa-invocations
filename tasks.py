import invoke

from saritasa_invocations import (
    celery,
    django,
    docker,
    fastapi,
    git,
    github_actions,
    open_api,
    pre_commit,
    python,
    system,
)

ns = invoke.Collection(
    celery,
    django,
    docker,
    fastapi,
    git,
    github_actions,
    open_api,
    pre_commit,
    python,
    system,
)

# Configurations for run command
ns.configure(
    dict(
        run=dict(
            pty=True,
            echo=True,
        ),
        saritasa_invocations={
            "project_name": "saritasa_invocations",
            "pre_commit_hooks": (
                "pre-commit",
                "pre-push",
                "commit-msg",
            ),
        },
    ),
)
