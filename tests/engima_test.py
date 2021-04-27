import pytest

from enigma_simulator import Enigma


@pytest.mark.parametrize(
    ("message", "expected"),
    (
        pytest.param("HELLOXWORLD", "MDCHVZFROTW", id="normal message"),
        pytest.param("", "", id="handles empty string"),
        pytest.param("toxcaps", "PWOOBUK", id="handles lower case"),
        pytest.param(
            "extremelyxlongxmessagextoxcheckxturnoverxandxdoublexstepping",
            "CSNWNLYKTZMVFPYNPJIOIGUYYLUISYOIMJSFRMBMOCUJZBQJJMMYDNSNKXDJ",
            id="turnover and double stepping",
        ),
    ),
)
def test_encryption(message, expected):
    enigma = Enigma(["I", "II", "III"], [3, 2, 25], [0, 0, 0], "B", "AD")
    encrypted = enigma.encrypt(message)

    assert encrypted == expected
