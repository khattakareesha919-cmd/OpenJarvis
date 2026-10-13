"""Startup banner: the Aston wordmark and a one-line tagline."""

from __future__ import annotations

# "Aston" rendered in the figlet "standard" font, generated with pyfiglet and
# pasted verbatim. Stored as plain text with no inline Rich markup, so the
# backslashes in the glyphs cannot collide with Rich's [tag] syntax; colour is
# applied at print time through a style argument instead.
_WORDMARK = (
    "    _        _              ",
    "   / \\   ___| |_ ___  _ __  ",
    "  / _ \\ / __| __/ _ \\| '_ \\ ",
    " / ___ \\\\__ \\ || (_) | | | |",
    "/_/   \\_\\___/\\__\\___/|_| |_|",
)

_TAGLINE = "At your service."

# Warm neutrals rather than the terminal's default blues. 180 is a pale brass,
# 101 a muted grey-brown that keeps the tagline behind the wordmark.
_WORDMARK_STYLE = "bold color(180)"
_TAGLINE_STYLE = "color(101)"


def print_banner(quiet: bool = False) -> None:
    """Print the Aston startup banner. No-op when quiet."""
    if quiet:
        return
    try:
        from rich.console import Console

        console = Console()
        for line in _WORDMARK:
            console.print(line, style=_WORDMARK_STYLE, highlight=False, markup=False)
        console.print(
            f"    {_TAGLINE}", style=_TAGLINE_STYLE, highlight=False, markup=False
        )
        console.print()
    except ImportError:
        for line in _WORDMARK:
            print(line)
        print(f"    {_TAGLINE}")
        print()
