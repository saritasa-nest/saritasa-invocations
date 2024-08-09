import json
import pathlib
import shutil

import invoke

from . import _config, printing


@invoke.task
def check_for_cruft_files(context: invoke.Context) -> None:
    """Check that there are no cruft files (`*.rej`)."""
    found_files = tuple(
        filter(
            lambda filepath: not filepath.startswith(".venv"),
            map(str, pathlib.Path().glob("**/*.rej")),
        ),
    )
    if not found_files:
        return
    found_files_str = "\n".join(found_files)
    printing.print_error(f"Found cruft files:\n{found_files_str}")
    raise invoke.Exit(
        code=1,
        message=(
            "You have `.rej` files present, "
            "please resolve conflicts with cruft!"
        ),
    )


def create_project(
    context: invoke.Context,
    project_folder_name: str,
    **questions,
) -> str:
    """Create cruft project.

    Utility shortcut for testing cruft boilerplates.

    """
    git_change = context.run(
        "git status . --porcelain",
        pty=False,
        hide="out",
    )
    if git_change and git_change.stdout:
        printing.print_warn(
            "Warning: you have uncommitted files in boilerplate. "
            "Cruft generates project from latest commit. \n"
            "Git status output:\n"
            f"{git_change.stdout}",
        )
    config = _config.Config.from_context(context)
    tmp_folder = config.cruft.project_tmp_folder
    printing.print_success(f"Recreating tmp ({tmp_folder}) folder")
    shutil.rmtree(tmp_folder, ignore_errors=True)
    pathlib.Path(tmp_folder).mkdir(parents=True, exist_ok=True)
    with context.cd(tmp_folder):
        context.run(
            "cruft create ../. --no-input --overwrite-if-exists "
            f"--extra-context '{json.dumps(questions)}'",
        )
    project_path = f"{tmp_folder}/{project_folder_name}"
    printing.print_success(f"Project is created at {project_path}")
    return project_path
