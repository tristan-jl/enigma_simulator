import numpy as np
import pytest

from enigma_simulator.utils import char_to_int
from enigma_simulator.utils import char_to_vec
from enigma_simulator.utils import encoding_to_transform
from enigma_simulator.utils import int_to_char
from enigma_simulator.utils import transform_to_encoding
from enigma_simulator.utils import vec_to_char


@pytest.mark.parametrize(
    ("char",),
    tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
)
def test_char_converters(char):
    _int = char_to_int(char)
    vec = char_to_vec(char)

    assert isinstance(_int, int)
    assert isinstance(vec, np.ndarray)
    assert int_to_char(_int) == char
    assert vec_to_char(vec) == char


@pytest.mark.parametrize(
    ("encoding",),
    (
        ("ABCDEFGHIJKLMNOPQRSTUVWXYZ",),
        ("YRUHQSLDPXNGOKMIEBFZCWVJAT",),
        ("BDFHJLCPRTXVZNYEIWGAKMUSQO",),
    ),
)
def test_encoding_converters(encoding):
    transform = encoding_to_transform(encoding)

    assert isinstance(transform, np.ndarray)
    assert transform_to_encoding(transform) == encoding
