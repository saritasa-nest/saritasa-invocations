import invoke

from saritasa_invocations import (
    docker,
    git,
    github_actions,
    pre_commit,
    system,
)

ns = invoke.Collection(
    docker,
    git,
    github_actions,
    pre_commit,
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
