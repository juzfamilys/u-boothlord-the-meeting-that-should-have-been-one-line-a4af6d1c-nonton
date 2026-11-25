"""The Meeting That Should Have Been One Line.

Writes one original line to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output):
the single sentence that could have replaced an entire pointless meeting.

Pure Python standard library only; no dependencies, no network, no I/O
outside the output directory. The entry is validated before and after
writing: 1-200 characters, a single line, no leading/trailing whitespace,
and byte-identical on re-read.
"""

import os
import sys

ENTRY = (
    "The client said yes, finance signed off, and the launch moved to "
    "Friday, so the only thing left on the agenda is who sends the email "
    "cancelling this meeting."
)


def validate(text):
    """Gate: 1-200 chars, UTF-8, not only whitespace, single line."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    if not 1 <= len(text) <= 200:
        raise ValueError("entry must be 1-200 characters, got %d" % len(text))
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        raise ValueError("entry must not have leading/trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")  # raises if not valid UTF-8-encodable
    return text


def verify_entry(path, entry):
    """Post-write gate: re-read entry.txt and re-validate every rule.

    Checks the file is byte-identical to the entry, still 1-200 chars,
    a single line, and free of leading/trailing whitespace. Raises
    SystemExit on any mismatch so a bad write never passes silently.
    """
    with open(path, "rb") as f:
        raw = f.read()
    if raw != entry.encode("utf-8"):
        raise SystemExit("entry.txt does not match the entry byte-for-byte")
    if len(raw) != len(entry.encode("utf-8")):
        raise SystemExit("entry.txt byte length changed: %d" % len(raw))
    text = raw.decode("utf-8")
    validate(text)
    if text != text.strip():
        raise SystemExit("entry.txt has leading/trailing whitespace")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry.txt is not a single line")
    return len(raw)


def run():
    entry = validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Write exactly the line, no trailing newline.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(entry)
    # Re-read and verify byte-identical output before reporting success.
    size = verify_entry(path, entry)
    print("wrote %d bytes to %s" % (size, path))
    return 0


if __name__ == "__main__":
    sys.exit(run())
