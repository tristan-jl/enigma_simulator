import pytest

from enigma_simulator.components import get_rotor
from enigma_simulator.utils import transform_to_encoding


def gen_data(encoding, position, ring_setting):
    encoding_list = list(encoding)
    for _ in range(position):
        encoding_list.append(encoding_list.pop(0))

    encoding_list = [
        chr((ord(c) - 65 - position + ring_setting) % 26 + 65) for c in encoding_list
    ]
    for _ in range(ring_setting):
        encoding_list.insert(0, encoding_list.pop())

    return "".join(encoding_list)


@pytest.mark.parametrize(
    "rotor_name", ("I", "II", "III", "IV", "V", "VI", "VII", "VIII")
)
@pytest.mark.parametrize("ring_setting", range(-1, 2))
@pytest.mark.parametrize("position", range(-1, 2))
def test_transform(rotor_name, ring_setting, position):
    ring_setting %= 26
    position %= 26
    rotor = get_rotor(rotor_name, ring_setting, position)
    encoding = rotor.initial_encoding

    assert transform_to_encoding(rotor.transform) == gen_data(
        encoding, position, ring_setting
    )
