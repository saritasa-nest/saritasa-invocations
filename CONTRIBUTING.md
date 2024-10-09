# How to contribute

## Dependencies

We use [poetry](https://github.com/python-poetry/poetry) to manage the dependencies.

To install them you would need to run `install` command:

```bash
poetry install
```

To activate your `virtualenv` run `poetry shell`.

## Style checks

We use `pre-commit` for quality control.

To run checks:

```bash
inv pre-commit.run-hooks
```

Note: we also have flake8 dependencies for proper support of flake8 vscode
plugin.

## Submitting your code

We use [trunk based](https://trunkbaseddevelopment.com/) development.

What the point of this method?

1. We use protected `main` branch,
   so the only way to push your code is via pull request
2. We use issue branches: to implement a new feature or to fix a bug
   create a new branch named `issue-$TASKNUMBER`
3. Then create a pull request to `main` branch
4. We use `git tag`s to make releases, so we can track what has changed
   since the latest release

So, this way we achieve an easy and scalable development process
which frees us from merging hell and long-living branches.

In this method, the latest version of the app is always in the `main` branch.

### Before submitting

Before submitting your code please do the following steps:

1. Add any changes you want
2. Edit documentation if you have changed something significant
3. Update `CHANGELOG.md` with a quick summary of your changes
4. Run `pre-commit` to ensure that style is correct
