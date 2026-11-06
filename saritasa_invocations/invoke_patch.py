import fcntl
import struct
import sys
import termios
import typing

import invoke.runners
import invoke.util


def bytes_to_read(input_: typing.IO[typing.Any]) -> int:
    """Return how many bytes can be read from `input_` right now.

    Copy of `invoke.terminals.bytes_to_read` with an int-sized `FIONREAD`
    buffer. Invoke passes 2 bytes and staring with Python 3.14 raises
    `SystemError: buffer overflow` on it, the stdin thread dies and
    interactive tasks (e.g. `inv django.shell`) ignore the keyboard.

    """
    is_terminal = (
        sys.platform != "win32"
        and invoke.util.isatty(input_)
        and invoke.util.has_fileno(input_)
    )
    if not is_terminal:
        return 1
    buffer = fcntl.ioctl(input_, termios.FIONREAD, bytes(4))
    return struct.unpack("i", buffer)[0]


if sys.version_info >= (3, 14):
    # Patch until the fix is released, then remove:
    # https://github.com/pyinvoke/invoke/issues/1052
    # https://github.com/pyinvoke/invoke/pull/1077
    invoke.runners.bytes_to_read = bytes_to_read
