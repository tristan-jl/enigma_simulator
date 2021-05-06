import io

import pytest

from enigma_simulator import output


def test_write():
    stream = io.BytesIO()
    output.write("hello world", stream)
    assert stream.getvalue() == b"hello world"


@pytest.mark.parametrize("input", (b"hello world", b"", None))
def test_write_line_bytes(input):
    stream = io.BytesIO()
    output.write_line_bytes(input, stream)
    assert stream.getvalue() == (input or b"") + b"\n"


@pytest.mark.parametrize("input", ("hello world", "", None))
def test_write_line(input):
    stream = io.BytesIO()
    output.write_line(input, stream)
    assert stream.getvalue() == (input or "").encode() + b"\n"
