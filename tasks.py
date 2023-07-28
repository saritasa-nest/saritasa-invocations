import invoke

import saritasa_invocations

ns = invoke.Collection(
    saritasa_invocations.alembic,
    saritasa_invocations.celery,
    saritasa_invocations.django,
    saritasa_invocations.docker,
    saritasa_invocations.fastapi,
    saritasa_invocations.git,
    saritasa_invocations.github_actions,
    saritasa_invocations.open_api,
    saritasa_invocations.pre_commit,
    saritasa_invocations.python,
    saritasa_invocations.system,
)

# Configurations for run command
ns.configure(
    dict(
        run=dict(
            pty=True,
            echo=True,
        ),
        saritasa_invocations=saritasa_invocations.Config(
            project_name="saritasa_invocations",
            pre_commit_hooks=(
                "pre-commit",
                "pre-push",
                "commit-msg",
            ),
        ),
    ),
)
