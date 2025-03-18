from dataclasses import dataclass
from typing import Self
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

    def __str__(self) -> str:
        return self.value

    def __add__(self, other) -> Self:
        if not isinstance(other, Element):
            return NotImplemented
        return Element(combine(self.value, other.value))

    def __mul__(self, other) -> Self:
        if not isinstance(other, int):
            return NotImplemented
        return Element(scale(self.value, other))

    def __rmul__(self, other) -> Self:
        return self.__mul__(other)

    def __invert__(self) -> Self:
        return Element(invert(self.value))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Element):
            return NotImplemented
        return self.value == other.value
