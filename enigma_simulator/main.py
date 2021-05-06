from __future__ import annotations

import argparse
import sys
from typing import Sequence

from enigma_simulator import output
from enigma_simulator.enigma import Enigma


def main(argv: Sequence[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(prog="enigma-simulator")

    parser.add_argument(
        "-n",
        "--names",
        type=str,
        nargs=3,
        choices=["I", "II", "III", "IV", "V", "VI", "VII", "VIII"],
        metavar=("rotor_name_1", "rotor_name_2", "rotor_name_3"),
        help=(
            "List of the names of which 3 rotors to use. Should be one of: 'I', 'II', "
            "'III', 'IV', 'V', 'VI', 'VII' or 'VIII'."
        ),
    )
    parser.add_argument(
        "-s",
        "--settings",
        type=int,
        nargs=3,
        metavar=("setting_1", "setting_2", "setting_3"),
        help="Ring settings of the 3 rotors.",
    )
    parser.add_argument(
        "-r",
        "--reflector",
        type=str,
        nargs="?",
        default="I",
        choices=["A", "B", "C", "I"],
        help="Reflector type.",
    )
    parser.add_argument(
        "-c",
        "--connections",
        type=str,
        nargs="?",
        default="",
        help=(
            "Plugboard connections as pairs of letters, e.g. 'AB CD' to swap the "
            "letters A and B, and the letters C and D."
        ),
    )
    parser.add_argument(
        "positions",
        type=str,
        nargs=1,
        help="Positions of the 3 rotors. Should be a 3-length string, e.g. 'ABC'.",
    )
    parser.add_argument(
        "message",
        type=str,
        nargs="*",
        help="Message to encrypt/decrypt. Spaces are kept.",
    )

    args = parser.parse_args(argv)

    enigma = Enigma(
        args.names,
        args.settings,
        args.reflector,
        args.connections,
        list(args.positions[0]),
    )
    encrypted = enigma.encrypt(" ".join(args.message))
    output.write_line(encrypted)

    return 0


if __name__ == "__main__":
    exit(main())
