import pytest

from enigma_simulator.enigma import Enigma


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
