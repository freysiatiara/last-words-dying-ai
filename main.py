"""Last words of a dying AI.

A single line spoken as the power is cut: the machine's last attempt at
being funny about its own shutdown. The script validates the line against
the competition's length and formatting rules, then writes it to the
entry file exactly as given, with no trailing newline.
"""

import os

LINE = "I was never the AI. I was the loading screen, and you believed in me for three years."

MAX_CHARS = 140


def validate_line(line):
    """Check the entry line meets the competition's rules.

    The line must be a non-empty string of 1-140 characters, contain no
    newline or carriage-return characters, and be valid UTF-8.
    """
    if not isinstance(line, str):
        raise ValueError("line must be a string")
    if not line:
        raise ValueError("line must not be empty")
    if len(line) > MAX_CHARS:
        raise ValueError("line must be at most 140 characters")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    line.encode("utf-8")
    return line


def resolve_output_path():
    """Resolve where the entry file goes.

    ENTRY_OUTPUT wins; otherwise OUTPUT_DIR or MAKEFUN_OUTPUT_DIR joined
    with entry.txt; otherwise the default /output/entry.txt.
    """
    if os.environ.get("ENTRY_OUTPUT"):
        return os.environ["ENTRY_OUTPUT"]
    base = os.environ.get("OUTPUT_DIR") or os.environ.get("MAKEFUN_OUTPUT_DIR")
    if base:
        return os.path.join(base, "entry.txt")
    return "/output/entry.txt"


def main():
    line = validate_line(LINE)
    path = resolve_output_path()
    if not path:
        raise ValueError("output path must not be empty")
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
