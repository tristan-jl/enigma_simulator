import numpy as np


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


def transform_to_encoding(transform: np.ndarray) -> str:
    encoding = ""

    for vec in transform.transpose():
        encoding += vec_to_char(vec)

    return encoding
