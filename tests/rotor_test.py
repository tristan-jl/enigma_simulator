import pytest

from enigma_simulator.components import Rotor
from enigma_simulator.utils import transform_to_encoding


@pytest.mark.parametrize(
    ("position", "ring_setting", "encoding", "notch_positions", "expected"),
    (
        pytest.param(
            0,
            0,
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            ["A"],
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            id="identity",
        ),
        pytest.param(
            1,
            0,
            "BACDEFGHIJKLMNOPQRSTUVWXYZ",
            ["A"],
            "ZBCDEFGHIJKLMNOPQRSTUVWXYA",
            id="ring positions",
        ),
        pytest.param(
            0,
            "B",
            "BACDEFGHIJKLMNOPQRSTUVWXYZ",
            ["A"],
            "CBDEFGHIJKLMNOPQRSTUVWXYZA",
            id="ring settings",
        ),
    ),
)
def test_transform(position, ring_setting, encoding, notch_positions, expected):
    rotor = Rotor("name", position, ring_setting, encoding, notch_positions)
    result_encoding = transform_to_encoding(rotor.transform)

    assert result_encoding == expected
