import numpy as np
import pytest

from enigma_simulator.components import Plugboard
from enigma_simulator.utils import transform_to_encoding


@pytest.mark.parametrize(
    ("encoding", "expected"),
    (
        pytest.param(
            "",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            id="identity",
        ),
        pytest.param(
            "AZ BY CX DW EV",
            "ZYXWVFGHIJKLMNOPQRSTUEDCBA",
            id="creates transform correctly",
        ),
    ),
)
def test_transform(encoding, expected):
    reflector = Plugboard(encoding)
    result_encoding = transform_to_encoding(reflector.transform)

    assert result_encoding == expected


def test_raises():
    with pytest.raises(RuntimeError):
        Plugboard("AB BC")
