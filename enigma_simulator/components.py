from __future__ import annotations

import re
import sys
from typing import Callable

import numpy as np
from numpy.linalg import matrix_power

from enigma_simulator.utils import char_to_int
from enigma_simulator.utils import encoding_to_transform

if sys.version_info >= (3, 8):  # pragma: no cover
    from typing import TypedDict
else:  # pragma: no cover
    from typing_extensions import TypedDict


WHITESPACE_REGEX = re.compile("[^a-zA-Z]")


class Component:
    def __init__(self, transform: np.ndarray) -> None:
        self.transform = transform
        self.transform_t = self.transform.transpose()

    def forward(self, x: np.ndarray) -> np.ndarray:
        return self.transform @ x

    def backward(self, x: np.ndarray) -> np.ndarray:
        return self.transform_t @ x

    __call__: Callable[..., np.ndarray] = forward


class Rotor(Component):
    def __init__(
        self,
        name: str,
        ring_setting: int,
        encoding: str,
        notch_positions: list[str],
        position: int | str,
    ) -> None:
        self.name = name
        self.ring_setting = ring_setting % 26

        if isinstance(position, int):
            self.position = position % 26
        elif isinstance(position, str):
            self.position = char_to_int(position)
        else:
            raise NotImplementedError

        self.notch_positions = [(char_to_int(i) - 1) % 26 for i in notch_positions]

        self.initial_encoding = encoding
        generated_transforms = self.generate_transforms(
            encoding_to_transform(encoding), self.ring_setting
        )
        self.transforms = {k: v for k, v in enumerate(generated_transforms)}
        self.transforms_t = {
            k: v.transpose() for k, v in enumerate(generated_transforms)
        }

    @property
    def at_notch(self) -> bool:
        return any(
            self.position == notch_position for notch_position in self.notch_positions
        )

    @property
    def transform(self) -> np.ndarray:  # type: ignore
        return self.transforms[self.position]

    @property
    def transform_t(self) -> np.ndarray:  # type: ignore
        return self.transforms_t[self.position]

    def turnover(self) -> None:
        self.position = (self.position + 1) % 26

    @staticmethod
    def generate_transforms(
        initial_transform: np.ndarray, ring_setting: int
    ) -> list[np.ndarray]:
        _list = list(range(26))
        _list.append(_list.pop(0))
        permutation = np.diag(np.ones(26, dtype=int))[_list]

        return [
            np.roll(
                matrix_power(permutation, i)
                @ initial_transform
                @ matrix_power(permutation, -i),
                (ring_setting, ring_setting),
                (0, 1),
            )
            for i in range(26)
        ]


class Reflector(Component):
    def __init__(self, encoding: str) -> None:
        if len(encoding) != 26:
            raise RuntimeError(
                f"Encoding should have 26 characters, not {len(encoding)}."
            )

        super().__init__(encoding_to_transform(encoding))
        self.transform_t = self.transform

    def backward(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError


class Plugboard(Component):
    def __init__(self, connections: str) -> None:
        super().__init__(self.connections_to_transform(connections))

    @staticmethod
    def connections_to_transform(connections: str) -> np.ndarray:
        transform = np.diag(np.ones(26, dtype=int))
        seen = set()

        if len(connections) > 0:
            for char_pair in re.split(WHITESPACE_REGEX, connections):
                c1, c2 = tuple(char_pair)

                if c1 in seen or c2 in seen:
                    raise RuntimeError(
                        f"Invalid connections. {c1} or {c2} is duplicated."
                    )

                seen.add(c1)
                seen.add(c2)
                i = char_to_int(c1)
                j = char_to_int(c2)

                transform[i][i] = 0
                transform[i][j] = 1
                transform[j][i] = 1
                transform[j][j] = 0

        return transform


def get_rotor(name: str, ring_setting: int, position: int) -> Rotor:
    class RotorAttribute(TypedDict):
        encoding: str
        notch_positions: list[str]

    rotor_setup: dict[str, RotorAttribute] = {
        "I": {
            "encoding": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
            "notch_positions": ["R"],
        },
        "II": {
            "encoding": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
            "notch_positions": ["F"],
        },
        "III": {
            "encoding": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
            "notch_positions": ["W"],
        },
        "IV": {
            "encoding": "ESOVPZJAYQUIRHXLNFTGKDCMWB",
            "notch_positions": ["K"],
        },
        "V": {
            "encoding": "VZBRGITYUPSDNHLXAWMJQOFECK",
            "notch_positions": ["A"],
        },
        "VI": {
            "encoding": "JPGVOUMFYQBENHZRDKASXLICTW",
            "notch_positions": ["A", "N"],
        },
        "VII": {
            "encoding": "NZJHGRCXMYSWBOUFAIVLPEKQDT",
            "notch_positions": ["A", "N"],
        },
        "VIII": {
            "encoding": "FKQHTLXOCBJSPDZRAMEWNIUYGV",
            "notch_positions": ["A", "N"],
        },
    }

    rotor_attrs: RotorAttribute = rotor_setup.get(
        name,
        {
            "encoding": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "notch_positions": ["A"],
        },
    )

    return Rotor(
        name,
        ring_setting,
        rotor_attrs["encoding"],
        rotor_attrs["notch_positions"],
        position,
    )


def get_reflector(reflector_type: str) -> Reflector:
    if reflector_type == "A":
        return Reflector("EJMZALYXVBWFCRQUONTSPIKHGD")
    elif reflector_type == "B":
        return Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
    elif reflector_type == "C":
        return Reflector("FVPJIAOYEDRZXWGCTKUQSBNMHL")
    else:
        return Reflector("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
