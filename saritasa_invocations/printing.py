import rich
import rich.console
import rich.panel
import rich.text


def print_panel(
    msg: rich.console.RenderableType,
    style: str,
    title: rich.text.TextType | None = None,
) -> None:
    """Print message in panel."""
    rich.print(
        rich.panel.Panel(
            msg,
            style=style,
            title=title,
        ),
    )


def print_success(
    msg: rich.console.RenderableType,
    title: rich.text.TextType | None = None,
) -> None:
    """Print success message."""
    print_panel(
        msg=msg,
        style="green bold",
        title=title,
    )


def print_warn(
    msg: rich.console.RenderableType,
    title: rich.text.TextType | None = None,
) -> None:
    """Print warning message."""
    print_panel(
        msg=msg,
        style="yellow bold",
        title=title,
    )


def print_error(
    msg: rich.console.RenderableType,
    title: rich.text.TextType | None = None,
) -> None:
    """Print error message."""
    print_panel(
        msg=msg,
        style="red bold",
        title=title,
    )
