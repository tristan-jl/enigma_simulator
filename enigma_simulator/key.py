from __future__ import annotations

import json
from enum import Enum
from typing import List

import yaml
from pydantic import BaseModel


class RotorNameEnum(str, Enum):
    one = "I"
    two = "II"
    three = "III"
    four = "IV"
    five = "V"
    six = "VI"
    seven = "VII"
    eight = "VIII"


class ReflectorTypeEnum(str, Enum):
    a = "A"
    b = "B"
    c = "C"
    i = "I"


class EnigmaKey(BaseModel):
    rotor_names: List[RotorNameEnum]
    ring_settings: List[int]
    reflector_type: ReflectorTypeEnum
    plugboard_connections: str = ""


def load_key(file_path: str) -> EnigmaKey:
    with open(file_path, "r") as f:
        if file_path[-5:] == ".json":
            key = json.load(f)
        elif file_path[-5:] == ".yaml" or file_path[-4:] == ".yml":
            key = yaml.safe_load(f)
        else:
            raise NotImplementedError

    return EnigmaKey.parse_obj(key)
