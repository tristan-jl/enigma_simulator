import numpy as np
import pytest

from enigma_simulator.components import get_reflector
from enigma_simulator.components import Reflector
from enigma_simulator.utils import transform_to_encoding


@pytest.mark.parametrize(
    ("encoding",),
    (
        pytest.param(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            id="identity",
        ),
        pytest.param(
            "YRUHQSLDPXNGOKMIEBFZCWVJAT",
            id="creates transform correctly",
        ),
    ),
)
def test_transform(encoding):
    reflector = Reflector(encoding)
    result_encoding = transform_to_encoding(reflector.transform)

    assert result_encoding == encoding


@pytest.mark.parametrize(
    (
        "reflector_type",
        "encoding",
    ),
    (
        pytest.param("A", "EJMZALYXVBWFCRQUONTSPIKHGD", id="reflector type A"),
        pytest.param("B", "YRUHQSLDPXNGOKMIEBFZCWVJAT", id="reflector type B"),
        pytest.param("C", "FVPJIAOYEDRZXWGCTKUQSBNMHL", id="reflector type C"),
        pytest.param(
            "other", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", id="reflector type default"
        ),
    ),
)
def test_get_reflector(reflector_type, encoding):
    reflector = get_reflector(reflector_type)
    result_encoding = transform_to_encoding(reflector.transform)

    assert result_encoding == encoding


def test_raises():
    with pytest.raises(RuntimeError):
        Reflector("bad encoding")
