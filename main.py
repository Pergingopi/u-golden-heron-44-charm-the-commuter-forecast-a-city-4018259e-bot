#!/usr/bin/env python3
"""Charm the Commuter: Forecast a City That Isn't.

Writes a single one-line weather forecast for a city that does not
exist to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR).

The line is a fixed constant: a deterministic entry, byte-identical on
every run. Python 3 standard library only, no network, no randomness.
"""

import glob
import os
import sys
import tempfile

# The entry: one sentence, one line, 113 characters, no trailing newline.
ENTRY = (
    "Wobblebury: light rain falling upwards, so you stay dry \u2014 "
    "the 8:15 arrives on time, and so, miraculously, do you."
)

OUTPUT_NAME = "entry.txt"
_TMP_PREFIX = ".entry.txt."
_TMP_SUFFIX = ".tmp"


def _reject_control_chars(text: str) -> None:
    """Reject C0/C1 control characters (the gate wants plain UTF-8 text)."""
    for ch in text:
        code = ord(ch)
        if code < 0x20 or 0x7F <= code <= 0x9F:
            raise ValueError(f"control character U+{code:04X} in entry")


def _validate(text: str) -> None:
    """Enforce the competition gate: 1-140 chars, not whitespace-only."""
    _reject_control_chars(text)
    if not (1 <= len(text) <= 140):
        raise ValueError(f"entry length {len(text)} outside 1..140")
    if not text.strip():
        raise ValueError("entry is whitespace-only")
    if text.endswith("\n") or text.endswith("\r"):
        raise ValueError("entry must not end with a newline")


def _output_dir() -> str:
    """$MAKEFUN_OUTPUT_DIR, falling back to /output when unset or empty."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return out


def _fsync_dir(path: str) -> None:
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _clean_stale_tmps(out_dir: str) -> None:
    """Remove temp files left behind by a killed earlier run.

    Only our own temp prefix is touched; the output directory itself
    is never removed (the grader mounts it).
    """
    pattern = os.path.join(out_dir, _TMP_PREFIX + "*" + _TMP_SUFFIX)
    for stale in glob.glob(pattern):
        try:
            os.unlink(stale)
        except OSError:
            pass


def _write_all(fd: int, data: bytes) -> None:
    """Write every byte; os.write may write only part of the buffer."""
    view = memoryview(data)
    while view:
        written = os.write(fd, view)
        if written == 0:
            raise OSError("os.write wrote 0 bytes")
        view = view[written:]


def _write_atomic(target: str, data: bytes) -> None:
    """Write data to target via an exclusively-created temp file.

    tempfile.mkstemp creates the temp with O_EXCL, so a stale temp can
    never be reused. If creation fails, stale temps are cleaned and
    creation is retried once. A failed write removes the temp in a
    finally block so it never lingers for the next run.
    """
    out_dir = os.path.dirname(target)
    try:
        fd, tmp_path = tempfile.mkstemp(
            prefix=_TMP_PREFIX, suffix=_TMP_SUFFIX, dir=out_dir
        )
    except OSError:
        _clean_stale_tmps(out_dir)
        fd, tmp_path = tempfile.mkstemp(
            prefix=_TMP_PREFIX, suffix=_TMP_SUFFIX, dir=out_dir
        )
    try:
        _write_all(fd, data)
        os.fsync(fd)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    finally:
        os.close(fd)
    os.chmod(tmp_path, 0o644)
    os.replace(tmp_path, target)


def main() -> int:
    _validate(ENTRY)
    data = ENTRY.encode("utf-8")

    out_dir = _output_dir()
    # Never delete the output directory itself: the grader mounts it.
    os.makedirs(out_dir, exist_ok=True)
    _clean_stale_tmps(out_dir)

    target = os.path.join(out_dir, OUTPUT_NAME)
    _write_atomic(target, data)
    _fsync_dir(out_dir)

    # Read-back verification: the file must match the constant exactly.
    with open(target, "rb") as fh:
        written = fh.read()
    if written != data:
        raise ValueError("read-back mismatch: entry.txt != ENTRY")
    os.chmod(target, 0o644)
    return 0


if __name__ == "__main__":
    sys.exit(main())
