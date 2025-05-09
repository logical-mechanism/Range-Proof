from dataclasses import dataclass, field
from typing import Self
from src.blake2b_224 import generate
from src.bls12_381 import field_order, g1_point, rng
from src.element import Element


@dataclass
class Commitment:
    """
    Commitment represents a cryptographic commitment used in zero-knowledge proofs.
    The commitment is a binding and hiding cryptographic construct that ensures
    the value is securely committed while keeping it hidden until revealed.

    The commitment is defined as c = r * g + v * h, where:
    - r is the randomness (also known as the blinding factor).
    - v is the value being committed to.
    - g and h are fixed elements in the elliptic curve group.

    Attributes:
        v (int): The value being committed to.
        r (int | None): The randomness used in the commitment. If not provided,
                        it is generated randomly.
        c (Element): The resulting commitment, computed as c = r * g + v * h.
    """

    v: int
    r: int | None = None

    c: Element = field(init=False)

    def __post_init__(self) -> None:
        # this are fixed inside of a commitment
        g = Element(g1_point(1))
        h = Element(g1_point(2))
        # unique to this commitment
        if self.r is None:
            self.r = rng()
        self.c = self.r * g + self.v * h

    def hash(self) -> str:
        return generate(self.c.value)

    def __str__(self) -> str:
        return f"Commitment(c={self.c}, r={self.r}, v={self.v})"

    def __add__(self, other) -> Self:
        if not isinstance(other, Commitment):
            return NotImplemented
        # Add the r values
        combined_r = (self.r + other.r) % field_order
        # Add the v values
        combined_v = (self.v + other.v) % field_order
        # Create a new Commitment instance with combined values
        return Commitment(combined_v, combined_r)

    def __sub__(self, other) -> Self:
        if not isinstance(other, Commitment):
            return NotImplemented
        # Add the r values
        combined_r = (self.r - other.r) % field_order
        # Add the v values
        combined_v = (self.v - other.v) % field_order
        # Create a new Commitment instance with combined values
        return Commitment(combined_v, combined_r)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Commitment):
            return NotImplemented
        return self.c == other.c and self.r == other.r and self.v == other.v

    def prove_knowledge_of_r(self, value: int) -> bool:
        v_commitment = Commitment(value, 0)
        r_commitment = self - v_commitment
        alpha = rng()
        alpha_commitment = Commitment(0, alpha)
        beta = generate(alpha_commitment.c.value + r_commitment.c.value)
        b = int(beta, 16)
        z = (alpha + b * self.r) % field_order
        z_commitment = Commitment(0, z)
        right = alpha_commitment.c + (b * r_commitment.c)
        return z_commitment.c.value == right.value
