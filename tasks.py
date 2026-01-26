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
    saritasa_invocations.db_k8s,
    saritasa_invocations.db,
    saritasa_invocations.k8s,
    saritasa_invocations.cruft,
    saritasa_invocations.poetry,
    saritasa_invocations.pip,
    saritasa_invocations.mypy,
    saritasa_invocations.pytest,
    saritasa_invocations.secrets,
)

# Configurations for run command
ns.configure(
    {
        "run": {
            "pty": True,
            "echo": True,
        },
        "saritasa_invocations": saritasa_invocations.Config(
            project_name="saritasa_invocations",
            pre_commit=saritasa_invocations.PreCommitSettings(
                entry="prek",
                default_hook_stage="pre-push",
            ),
        ),
    },
)
