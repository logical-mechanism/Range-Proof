# src/Registry/element.py
from dataclasses import dataclass

from src.blake2b_224 import generate
from src.bls12_381 import combine, compress, invert, scale, uncompress


@dataclass
class Element:
    value: str

    def compressed(self) -> str:
        return compress(self.value)

    def uncompressed(self) -> tuple:
        return uncompress(self.value)

    def hash(self) -> str:
        return generate(self.value)

    def __str__(self):
        return self.value

    def __add__(self, other):
        if not isinstance(other, Element):
            return NotImplemented
        return Element(combine(self.value, other.value))

    def __mul__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return Element(scale(self.value, other))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __invert__(self):
        return Element(invert(self.value))

    def __eq__(self, other):
        if not isinstance(other, Element):
            return NotImplemented
        return self.value == other.value
