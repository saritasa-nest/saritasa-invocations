import rich
import rich.console
import rich.panel


def print_panel(
    msg: rich.console.RenderableType,
    style: str,
) -> None:
    """Print message in panel."""
    rich.print(
        rich.panel.Panel(
            msg,
            style=style,
        ),
    )


def print_success(msg: rich.console.RenderableType) -> None:
    """Print success message."""
    print_panel(
        msg=msg,
        style="green bold",
    )


def print_warn(msg: rich.console.RenderableType) -> None:
    """Print warning message."""
    print_panel(
        msg=msg,
        style="yellow bold",
    )


def print_error(msg: rich.console.RenderableType) -> None:
    """Print error message."""
    print_panel(
        msg=msg,
        style="red bold",
    )
