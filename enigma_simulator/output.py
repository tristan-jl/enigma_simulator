from __future__ import annotations

import sys
from typing import IO


def write(s: str, stream: IO[bytes] = sys.stdout.buffer) -> None:
    stream.write(s.encode())
    stream.flush()


def write_line_bytes(
    s: bytes | None = None, stream: IO[bytes] = sys.stdout.buffer
) -> None:
    if s is not None:
        stream.write(s)
    stream.write(b"\n")
    stream.flush()


def write_line(s: str | None = None, stream: IO[bytes] = sys.stdout.buffer) -> None:
    write_line_bytes(s.encode() if s is not None else s, stream)
