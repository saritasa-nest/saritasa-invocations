import collections.abc
import pathlib
import re

import invoke

from . import _config, pre_commit, printing


@invoke.task
def setup(context: invoke.Context) -> None:
    """Set up git for working."""
    printing.print_success("Setting up git and pre-commit")
    pre_commit.install(context)

    config = _config.Config.from_context(context)
    set_git_setting(
        context,
        setting="merge.ff",
        value=config.git.merge_ff,
    )
    set_git_setting(
        context,
        setting="pull.ff",
        value=config.git.pull_ff,
    )


def set_git_setting(
    context: invoke.Context,
    setting: str,
    value: str,
) -> None:
    """Set git setting in config."""
    context.run(f"git config --local --add {setting} {value}")


@invoke.task
def clone_repo(
    context: invoke.Context,
    repo_link: str,
    repo_path: str | pathlib.Path,
    branch: str = "",
    clone_params: str = "",
    pull_params: str = "",
    checkout_params: str = "",
) -> None:
    """Clone repo for work to folder."""
    if not pathlib.Path(repo_path).exists():
        printing.print_success(
            f"Cloning `{repo_link}` repository to `{repo_path}`",
        )
        context.run(f"git clone {repo_link} {repo_path} {clone_params}")
        checkout_to_branch(
            context,
            repo_path=repo_path,
            branch=branch,
            checkout_params=checkout_params,
        )
        printing.print_success(f"Successfully cloned to `{repo_path}`")
    else:
        printing.print_success(
            f"Pulling changes for `{repo_link}` in `{repo_path}`",
        )
        checkout_to_branch(
            context,
            repo_path=repo_path,
            branch=branch,
            checkout_params=checkout_params,
        )
        with context.cd(repo_path):
            context.run(f"git pull {pull_params}")


def checkout_to_branch(
    context: invoke.Context,
    repo_path: str | pathlib.Path,
    branch: str,
    checkout_params: str = "",
) -> None:
    """Checkout to repo's branch."""
    if not branch:
        return
    with context.cd(repo_path):
        printing.print_success(f"Checkout to `{branch}` branch")
        context.run(f"git checkout {branch} {checkout_params}")


@invoke.task
def blame_copy(
    context: invoke.Context,
    original_path: str,
    destination_paths: str,
) -> None:
    """Copy file from original path to destination paths with saving blame.

    If destination path is file, then data will be copied in it.
    If destination path is directory, then data will be copied in provided
    directory with original name.
    How script works:
        1) Remember current HEAD state
        2) For each copy path:
            move file to copy path, restore file using `checkout`,
            remember result commits
        3) Restore state of branch
        4) Move file to temp file
        5) Merge copy commits to branch
        6) Move file to it's original path from temp file
    Count of created commits:
        N + 3, where N - is count of copies,
        3 - 1 commit to put original file to temp file
        1 commit to merge commits with creation of copy files
        1 commit to put data from temp file to original file back.

    """
    config = _config.Config.from_context(context)
    destination_paths_list = _split_destination_paths(destination_paths)
    printing.print_success("Validating provided paths")
    _validate_paths(original_path, destination_paths_list)
    printing.print_success(
        config.git.copy_init_message_template.format(
            original_path=original_path,
            destination_paths="\n* ".join(destination_paths_list),
            commits_count=len(destination_paths_list) + 3,
        ),
    )
    _display_continue_prompt()
    # formatted commit template with only space for action
    printing.print_success("Build formatted commit")
    formatted_commit_template = config.git.copy_commit_template.format(
        action="{action}",
        original_path=original_path,
        destination_paths="\n* ".join(destination_paths_list),
        project_task=_build_task_string(context=context),
    )

    # temp file to save original file
    printing.print_success("Create temp file")
    temp_file = _get_command_output(
        context=context,
        command=f"mktemp ./{destination_paths_list[0]}.XXXXXX",
    )

    # current HEAD state
    printing.print_success("Get current HEAD sha")
    root_commit = _get_command_output(
        context=context,
        command="git rev-parse HEAD",
    )

    # create copies with blame of original
    printing.print_success("Create copies with blame of original file")
    copy_commits = _copy_files(
        context=context,
        original_path=original_path,
        destination_paths=destination_paths_list,
        root_commit=root_commit,
        commit_template=formatted_commit_template,
    )

    # put original file to temp copy
    printing.print_success("Restore branch to original state")
    context.run("git reset --hard HEAD^")
    printing.print_success(f"Move {original_path} to temp file")
    _move_file(
        context=context,
        from_path=original_path,
        to_path=temp_file,
        options=["-f"],
        message=formatted_commit_template.format(
            action=f"put {original_path} to temp file",
        ),
    )

    # merge copy commits
    printing.print_success("Merge copy commits")
    _merge_commits(
        context=context,
        commits=copy_commits,
        message=formatted_commit_template.format(action="merge"),
    )

    # move original file back
    printing.print_success(f"Move data from temp file to {original_path}")
    _move_file(
        context=context,
        from_path=temp_file,
        to_path=original_path,
        message=formatted_commit_template.format(
            action=f"put temp file data to {original_path}",
        ),
    )
    printing.print_success("Success")


def _split_destination_paths(
    destination_paths: str,
) -> list[str]:
    """Split destination path to sequence and strip trailing symbols."""
    return [path.strip() for path in destination_paths.split(",")]


def _validate_paths(
    original_path: str,
    destination_paths: collections.abc.Sequence[str],
) -> None:
    """Validate provided paths exists."""
    error_messages = []
    if not pathlib.Path(original_path).exists():
        error_messages.append(
            f"{original_path} not found.",
        )
    for destination in destination_paths:
        dirname = pathlib.Path(destination).parent
        if dirname and not pathlib.Path(dirname).exists():
            error_messages.append(f"{dirname} not found.")
    if error_messages:
        printing.print_error(
            "\n".join(error_messages),
        )
        raise invoke.Exit(
            message="Failed to validate provided paths.",
            code=1,
        )


def _merge_commits(
    context: invoke.Context,
    commits: collections.abc.Sequence[str],
    message: str,
) -> None:
    """Merge passed commits."""
    context.run(
        f"git merge {' '.join(commits)} -m '{message}'",
        warn=True,
    )
    # create commit in case if merge conflict occurs
    context.run(
        f"git commit --no-verify -a -n -m '{message}'",
    )


def _move_file(
    context: invoke.Context,
    from_path: str,
    to_path: str,
    message: str,
    options: collections.abc.Sequence[str] = (),
) -> None:
    """Move `first_file `to `second_file` path using git."""
    context.run(f"git mv {' '.join(options)} {from_path} {to_path}")
    context.run(f"git commit --no-verify -n -m '{message}'")


def _copy_files(
    context: invoke.Context,
    original_path: str,
    destination_paths: collections.abc.Sequence[str],
    root_commit: str,
    commit_template: str,
) -> list[str]:
    """Copy file from `original_path` to `destination_paths` using git.

    Return commits related to each copy.

    """
    commits = []
    for path in destination_paths:
        context.run(f"git reset --soft {root_commit}")
        context.run(f"git checkout {root_commit} {original_path}")
        context.run(f"git mv -f {original_path} {path}")

        commit_message = commit_template.format(
            action=f"create {path}",
        )
        context.run(f"git commit --no-verify -n -m '{commit_message}'")
        new_commit = _get_command_output(
            context=context,
            command="git rev-parse HEAD",
        )
        commits.append(new_commit)
    return commits


def _build_task_string(
    context: invoke.Context,
) -> str:
    """Build task string.

    Build string with following format: Task: <project-task-id>
    If current git branch has no task id, then empty string will return.

    """
    task_id = _get_project_task_from_current_branch(context=context)
    if not task_id:
        return ""
    return f"Task: {task_id}"


def _get_project_task_from_current_branch(
    context: invoke.Context,
) -> str:
    """Get project task from current branch.

    If branch has no task, then empty string will return.

    """
    current_branch = _get_command_output(
        context=context,
        command="git branch --show-current",
    )
    match = re.search(r"\w+\/(\w+-\d+)", current_branch)
    if match is None:
        return ""
    task = match.group(1)
    return task


def _display_continue_prompt() -> None:
    """Display continue message.

    If `n` entered, then exit script.

    """
    if input("Continue? [Enter/N]: ").lower() == "n":
        raise invoke.Exit("Exit from script", code=1)


def _get_command_output(
    context: invoke.Context,
    command: str,
) -> str:
    """Get command output.

    Try to run command using context.
    If no result returned then cancel command execution.

    """
    command_result = context.run(command)
    if command_result is None:
        raise invoke.Exit(
            code=1,
            message=(
                "Something went wrong.\n"
                "Make sure you have enough system permissions."
            ),
        )
    return command_result.stdout.rstrip()
