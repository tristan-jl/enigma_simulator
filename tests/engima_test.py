import numpy as np
import pytest

from enigma_simulator.enigma import create_enigma_from_key
from enigma_simulator.enigma import Enigma
from enigma_simulator.key import EnigmaKey
from enigma_simulator.key import load_key
from enigma_simulator.key import ReflectorTypeEnum
from enigma_simulator.key import RotorNameEnum


@pytest.mark.parametrize(
    ("message", "expected"),
    (
        pytest.param("AAAAA", "EWTYX", id="simple message"),
        pytest.param("HELLOXWORLD", "LOFUHZZLZOM", id="hello world"),
        pytest.param("", "", id="handles empty string"),
        pytest.param("toxcaps", "PESEXKY", id="handles lower case"),
    ),
)
def test_encryption(message, expected):
    enigma = Enigma(["I", "II", "III"], [1, 1, 1], "B", "", ["A", "A", "A"])
    encrypted = enigma.encrypt(message)

    assert encrypted == expected


def test_turnover_and_double_stepping():
    enigma = Enigma(["I", "II", "III"], [1, 1, 1], "B", "", ["Z", "Z", "Z"])
    message = (
        "Tomorrow and tomorrow and tomorrow Creeps in this petty pace from day to day "
        "To the last syllable of recorded time And all our yesterdays have lighted "
        "fools The way to dusty death Out out brief candle Lifes but a walking shadow "
        "a poor player That struts and frets his hour upon the stage And then is heard "
        "no more It is a tale Told by an idiot full of sound and fury Signifying "
        "nothing"
    )

    encrypted = enigma.encrypt(message)

    assert encrypted == (
        "MCDDJUXX CJJ JIHHBBLX ZTS KWSSNDHR AMWKIY JP BIDH BOKYL NGZW PATP GIA EI TCM "
        "MX NXJ CGHW EGNTOJXB TL JDHINBRZ HRNJ HCV RBA UHF MUILKNUMLO VXNA PRZCCNL "
        "QCCCA MBP CNJ VQ XWYVS KJRML ECE QHE KGUCO JJHCJM FEPSX FOA C LOUGDOO EZOSIG "
        "Y CTMJ MOFPIS WBTX NAHXIZ RUK ZGKXI VSF BWKU CVWH NZK TKDMW WHK MCFX JC PKCYI "
        "IJ KWGP OH FC N PLTF ZRIA YH XT BJOHA SOVG WX GSZMZ GSJ AKVZ QTVWSAPOYZ "
        "VKBTRCO"
    )


def test_update_enigma_rotor_positions():
    enigma = Enigma(["I", "II", "III"], [1, 1, 1], "B", "", [0, 0, 0])
    encrypted1 = enigma.encrypt("A")

    enigma.update_rotor_positions([0, 0, 0])
    encrypted2 = enigma.encrypt("A")

    assert encrypted1 == encrypted2 == "E"


def test_enigma_transmission_encryption():
    start_position, message_key, message = "WZA", "SXT", "HELLOHOWAREYOU"
    enigma = Enigma(["I", "II", "III"], [1, 1, 1], "B", "AB FD CH LO PW", [0, 0, 0])
    transmission = enigma.encrypt_transmission(message, start_position, message_key)

    assert transmission == ("WZA", "IGI", "EVIVKEGIPXXOQZ")


def test_enigma_transmission_encryption_provides_defaults():
    message = "HELLOHOWAREYOU"
    enigma = Enigma(["I", "II", "III"], [1, 1, 1], "B", "AB FD CH LO PW", [0, 0, 0])
    transmission = enigma.encrypt_transmission(message)

    assert len(transmission[0]) == 3
    assert len(transmission[1]) == 3
    assert len(transmission[2]) == len(message)


def test_enigma_transmission_decryption():
    start_position, encrypted_key, message = "WZA", "IGI", "EVIVKEGIPXXOQZ"
    enigma = Enigma(["I", "II", "III"], [1, 1, 1], "B", "AB FD CH LO PW", [0, 0, 0])
    transmission = enigma.decrypt_transmission(start_position, encrypted_key, message)

    assert transmission == "HELLOHOWAREYOU"


def test_create_enigma_from_key():
    rotor_names = [RotorNameEnum.one, RotorNameEnum.two, RotorNameEnum.three]
    ring_settings = [1, 2, 3]
    reflector_type = ReflectorTypeEnum.b
    plugboard_connections = "AB GD"

    enigma_key = EnigmaKey(
        rotor_names=rotor_names,
        ring_settings=ring_settings,
        reflector_type=reflector_type,
        plugboard_connections=plugboard_connections,
    )

    enigma = create_enigma_from_key(enigma_key)

    assert enigma.left_rotor.name == rotor_names[0]
    assert enigma.middle_rotor.name == rotor_names[1]
    assert enigma.right_rotor.name == rotor_names[2]

    assert enigma.left_rotor.ring_setting == ring_settings[0]
    assert enigma.middle_rotor.ring_setting == ring_settings[1]
    assert enigma.right_rotor.ring_setting == ring_settings[2]

    assert isinstance(enigma.reflector.transform, np.ndarray)
    assert isinstance(enigma.plugboard.transform, np.ndarray)


@pytest.mark.parametrize(
    ("file_type", "contents"),
    (
        (
            "json",
            """{
    "rotor_names": [
        "I",
        "II",
        "III"
    ],
    "ring_settings": [
        1,
        4,
        6
    ],
    "reflector_type": "B",
    "plugboard_connections": "AB NK"
}
""",
        ),
        (
            "yaml",
            """rotor_names:
  - "I"
  - "II"
  - "III"
ring_settings:
  - 1
  - 4
  - 6
reflector_type: B
plugboard_connections: "AB NK"
""",
        ),
    ),
)
def test_load_key(tmpdir, file_type, contents):
    p = tmpdir / f"test.{file_type}"
    p.write_text(contents, encoding=None)
    assert load_key(str(p)) == EnigmaKey(
        rotor_names=["I", "II", "III"],
        ring_settings=[1, 4, 6],
        reflector_type="B",
        plugboard_connections="AB NK",
    )
