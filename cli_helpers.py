"""CLI utilities for progress bars, colors, and terminal output."""

import sys
import time
from typing import Any, Iterable, Iterator


# ANSI color codes
class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"

    # Regular colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Background colors
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"


def colorize(text: str, color: str, bold: bool = False) -> str:
    """Add ANSI color codes to text.

    Args:
        text: Text to colorize
        color: Color code from Colors class
        bold: Make text bold

    Returns:
        Colorized string
    """
    prefix = Colors.BOLD if bold else ""
    return f"{prefix}{color}{text}{Colors.RESET}"


def red(text: str, bold: bool = False) -> str:
    """Make text red."""
    return colorize(text, Colors.RED, bold)


def green(text: str, bold: bool = False) -> str:
    """Make text green."""
    return colorize(text, Colors.GREEN, bold)


def yellow(text: str, bold: bool = False) -> str:
    """Make text yellow."""
    return colorize(text, Colors.YELLOW, bold)


def blue(text: str, bold: bool = False) -> str:
    """Make text blue."""
    return colorize(text, Colors.BLUE, bold)


def cyan(text: str, bold: bool = False) -> str:
    """Make text cyan."""
    return colorize(text, Colors.CYAN, bold)


class ProgressBar:
    """Simple progress bar for terminal output."""

    def __init__(
        self,
        total: int,
        prefix: str = "",
        suffix: str = "",
        width: int = 40,
        fill: str = "█",
        empty: str = "░",
    ):
        """Initialize progress bar.

        Args:
            total: Total number of items
            prefix: Text before the bar
            suffix: Text after the bar
            width: Width of the bar in characters
            fill: Character for completed portion
            empty: Character for remaining portion
        """
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.width = width
        self.fill = fill
        self.empty = empty
        self.current = 0
        self.start_time = time.time()

    def update(self, amount: int = 1) -> None:
        """Update progress by amount."""
        self.current = min(self.current + amount, self.total)
        self._display()

    def set(self, value: int) -> None:
        """Set progress to specific value."""
        self.current = min(value, self.total)
        self._display()

    def _display(self) -> None:
        """Display the progress bar."""
        percent = self.current / self.total if self.total > 0 else 0
        filled_width = int(self.width * percent)
        bar = self.fill * filled_width + self.empty * (self.width - filled_width)

        elapsed = time.time() - self.start_time
        if self.current > 0 and self.current < self.total:
            eta = (elapsed / self.current) * (self.total - self.current)
            time_str = f" ETA: {eta:.0f}s"
        else:
            time_str = f" {elapsed:.1f}s"

        line = f"\r{self.prefix}|{bar}| {self.current}/{self.total} ({percent:.0%}){time_str} {self.suffix}"
        sys.stdout.write(line)
        sys.stdout.flush()

        if self.current >= self.total:
            sys.stdout.write("\n")

    def finish(self) -> None:
        """Mark progress as complete."""
        self.current = self.total
        self._display()


def progress_iter(
    iterable: Iterable[Any],
    total: int | None = None,
    prefix: str = "",
) -> Iterator[Any]:
    """Wrap an iterable with a progress bar.

    Args:
        iterable: Items to iterate over
        total: Total count (auto-detect if possible)
        prefix: Text before progress bar

    Yields:
        Items from the iterable
    """
    if total is None:
        try:
            total = len(iterable)
        except TypeError:
            iterable = list(iterable)
            total = len(iterable)

    bar = ProgressBar(total, prefix=prefix)

    for item in iterable:
        yield item
        bar.update()


def confirm(prompt: str, default: bool = False) -> bool:
    """Ask user for yes/no confirmation.

    Args:
        prompt: Question to ask
        default: Default answer if user just presses Enter

    Returns:
        True for yes, False for no
    """
    suffix = " [Y/n]: " if default else " [y/N]: "
    response = input(prompt + suffix).strip().lower()

    if not response:
        return default

    return response in ("y", "yes", "true", "1")


def print_table(
    data: list[dict[str, Any]],
    headers: list[str] | None = None,
) -> None:
    """Print data as a simple ASCII table.

    Args:
        data: List of dicts to print
        headers: Column headers (auto-detect if None)
    """
    if not data:
        return

    if headers is None:
        headers = list(data[0].keys())

    # Calculate column widths
    widths = {h: len(h) for h in headers}
    for row in data:
        for h in headers:
            val = str(row.get(h, ""))
            widths[h] = max(widths[h], len(val))

    # Print header
    header_line = " | ".join(h.ljust(widths[h]) for h in headers)
    separator = "-+-".join("-" * widths[h] for h in headers)
    print(header_line)
    print(separator)

    # Print rows
    for row in data:
        row_line = " | ".join(str(row.get(h, "")).ljust(widths[h]) for h in headers)
        print(row_line)
