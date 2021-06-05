from __future__ import annotations

import re

import numpy as np

from enigma_simulator.components import get_reflector
from enigma_simulator.components import get_rotor
from enigma_simulator.components import Plugboard
from enigma_simulator.key import EnigmaKey
from enigma_simulator.utils import char_to_int
from enigma_simulator.utils import char_to_vec
from enigma_simulator.utils import int_to_char
from enigma_simulator.utils import vec_to_char

WHITESPACE_REGEX = re.compile("[^a-zA-Z]")


class Enigma:
    def __init__(
        self,
        rotor_names: list[str],
        ring_settings: list[int],
        reflector_type: str,
        plugboard_connections: str,
        rotor_positions: list[int] | list[str],
    ) -> None:
        self.left_rotor, self.middle_rotor, self.right_rotor = tuple(
            get_rotor(*i) for i in zip(rotor_names, ring_settings, rotor_positions)
        )
        self.reflector = get_reflector(reflector_type)
        self.plugboard = Plugboard(plugboard_connections)

    def encrypt(
        self,
        message: str,
        *,
        leave_whitespace=True,
    ) -> str:
        encrypted = ""
        for char in list(message):
            if leave_whitespace:
                if WHITESPACE_REGEX.match(char):
                    encrypted += char
                    continue

            self.rotate()

            vec = char_to_vec(char)
            vec = self.plugboard.forward(vec)
            vec = self.right_rotor.forward(vec)
            vec = self.middle_rotor.forward(vec)
            vec = self.left_rotor.forward(vec)
            vec = self.reflector.forward(vec)
            vec = self.left_rotor.backward(vec)
            vec = self.middle_rotor.backward(vec)
            vec = self.right_rotor.backward(vec)
            vec = self.plugboard.forward(vec)
            char = vec_to_char(vec)

            encrypted += char

        return encrypted

    def encrypt_transmission(
        self,
        message: str,
        *,
        start_position: str | None = None,
        message_key: str | None = None,
        leave_whitespace=True,
    ) -> tuple[str, str, str]:
        if start_position is None:
            rand_ints = np.random.randint(0, 26, size=3)
            _start_position = "".join(int_to_char(i) for i in rand_ints)
            self.update_rotor_positions(rand_ints)
        else:
            _start_position = start_position
            self.update_rotor_positions(start_position)

        if message_key is None:
            _message_key = "".join(
                int_to_char(i) for i in np.random.randint(0, 26, size=3)
            )
            encrypted_key = self.encrypt(_message_key)
        else:
            _message_key = message_key
            encrypted_key = self.encrypt(message_key)

        self.update_rotor_positions(_message_key)

        return (
            _start_position,
            encrypted_key,
            self.encrypt(message, leave_whitespace=leave_whitespace),
        )

    def decrypt_transmission(
        self, start_position: str, encrypted_key: str, message: str
    ) -> str:
        self.update_rotor_positions(start_position)
        key = self.encrypt(encrypted_key)
        self.update_rotor_positions(key)

        return self.encrypt(message)

    def rotate(self) -> None:
        if self.middle_rotor.at_notch:
            self.middle_rotor.turnover()
            self.left_rotor.turnover()
        elif self.right_rotor.at_notch:
            self.middle_rotor.turnover()

        self.right_rotor.turnover()

    def update_rotor_positions(self, rotor_positions: list[int] | str) -> None:
        if isinstance(rotor_positions, str):
            _rotor_positions = [char_to_int(c) for c in list(rotor_positions)]
        else:
            _rotor_positions = rotor_positions

        (
            self.left_rotor.position,
            self.middle_rotor.position,
            self.right_rotor.position,
        ) = tuple(_rotor_positions)


def create_enigma_from_key(
    key: EnigmaKey, rotor_positions: list[int] = [0, 0, 0]
) -> Enigma:
    return Enigma(
        [i for i in key.rotor_names],
        key.ring_settings,
        key.reflector_type,
        key.plugboard_connections,
        rotor_positions,
    )
