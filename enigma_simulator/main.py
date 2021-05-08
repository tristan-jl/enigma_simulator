from __future__ import annotations

import argparse
import sys
from typing import Sequence

from enigma_simulator import output
from enigma_simulator.enigma import create_enigma_from_key
from enigma_simulator.enigma import Enigma
from enigma_simulator.key import load_key


def main(argv: Sequence[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(
        prog="enigma-simulator",
        description=(
            "Encrypt or decrypt a simple message or transmission using a simulated "
            "Enigma machine. The settings of the machine can be passed in "
            "individually, or can pass in an 'Enigma key' file (see below)."
        ),
    )

    parser.add_argument(
        "-k",
        "--key",
        type=str,
        nargs=1,
        help="Path to key file. Must be a json or a yaml file.",
    )
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

    subparsers = parser.add_subparsers(help="sub-command help")

    message_parser = subparsers.add_parser(
        "message", help="Encrypt or decrypt a simple message."
    )
    message_parser.add_argument(
        "positions",
        type=str,
        nargs=1,
        help="Positions of the 3 rotors. Should be a 3-length string, e.g. 'ABC'.",
    )
    message_parser.add_argument(
        "message",
        type=str,
        nargs="*",
        help="Message to encrypt/decrypt. Spaces are kept.",
    )

    transmission_parser = subparsers.add_parser(
        "transmission",
        help="Encrypt or decrypt a transmission. See README for details.",
    )
    transmission_parser.add_argument(
        "-p",
        "--positions",
        type=str,
        nargs="?",
        help="Positions of the 3 rotors. Should be a 3-length string, e.g. 'ABC'.",
    )
    transmission_parser.add_argument(
        "-m",
        "--message-key",
        type=str,
        nargs="?",
        help="Secret message key. Should be a 3-length string, e.g. 'ABC'.",
    )
    transmission_parser.add_argument(
        "message",
        type=str,
        nargs="*",
        help="Message to encrypt/decrypt. Spaces are kept.",
    )
    group = transmission_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--encrypt", action="store_true", help="Encryption mode.")
    group.add_argument("--decrypt", action="store_false", help="Decryption mode.")

    args = parser.parse_args(argv)

    if args.key:
        enigma_key = load_key(args.key[0])
        enigma = create_enigma_from_key(enigma_key)

    else:
        positions = (
            list(
                args.positions[0]
                if isinstance(args.positions, list)
                else args.positions
            )
            if args.positions is not None
            else ["A", "A", "A"]
        )
        enigma = Enigma(
            args.names,
            args.settings,
            args.reflector,
            args.connections,
            positions,
        )

    message = " ".join(args.message)

    if "encrypt" in args:  # transmission
        print(args.positions, args.message_key, message)
        if args.encrypt:
            output.write_line(
                " ".join(
                    enigma.encrypt_transmission(
                        message, args.positions, args.message_key
                    )
                )
            )
        else:
            output.write_line(
                enigma.decrypt_transmission(args.positions, args.message_key, message)
            )

    else:
        encrypted = enigma.encrypt(message)
        output.write_line(encrypted)

    return 0


if __name__ == "__main__":
    exit(main())
