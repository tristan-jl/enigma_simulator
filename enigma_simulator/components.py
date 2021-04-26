from __future__ import annotations

import re
from typing import Callable
from typing import TypedDict

import numpy as np
from numpy.linalg import matrix_power

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
        position: int,
        ring_setting: int | str,
        encoding: str,
        notch_positions: list[str],
    ) -> None:
        self.name = name
        self.position = position % 26

        if isinstance(ring_setting, int):
            self.ring_setting = ring_setting % 26
        elif isinstance(ring_setting, str):
            self.ring_setting = char_to_int(ring_setting)
        else:
            raise NotImplementedError

        self.notch_positions = [(char_to_int(i) - 1) % 26 for i in notch_positions]

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
            (
                matrix_power(permutation, i - ring_setting)
                @ initial_transform
                @ matrix_power(permutation, -i)
            ).astype(int)
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


def get_rotor(name: str, position: int, ring_setting: int) -> Rotor:
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
        position,
        ring_setting,
        rotor_attrs["encoding"],
        rotor_attrs["notch_positions"],
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


def char_to_vec(c: str) -> np.ndarray:
    v = np.zeros(26, dtype=int)
    v[ord(c.upper()) - 65] = 1
    return v


def vec_to_char(v: np.ndarray) -> str:
    return chr(np.where(v == 1)[0][0] + 65)


def char_to_int(c: str) -> int:
    return ord(c.upper()) - 65


def int_to_char(i: int) -> str:
    return chr(i + 65)


def encoding_to_transform(encoding: str) -> np.ndarray:
    return np.array([char_to_vec(c) for c in encoding]).transpose()
