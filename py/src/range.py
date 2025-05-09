from dataclasses import dataclass, field

from src.blake2b_224 import fiat_shamir_heuristic, generate
from src.bls12_381 import field_order, g2_point, invert, pair, rng
from src.commitment import Commitment
from src.element import Element
from src.util import hexify


@dataclass
class Range:
    """
    Range is a cryptographic class for generating and verifying range proofs
    using BLS12-381 elliptic curve operations. If the lower and upper bounds
    are not provided they are assume to be 0 and the field prime. The proof
    solves a + b + w = y + 2d, assuming a - d = y and d - b = w, such that the
    equality a > d > b holds.

    It is assumed that the lower and upper bound values are public.

    Attributes:
        secret_value (int): The value to be proven within the range.
        lower_bound (int | None): The lower bound of the range.
        upper_bound (int | None): The upper bound of the range.
    """

    secret_value: int
    lower_bound: int | None = None
    upper_bound: int | None = None

    A_commit: Commitment = field(init=False)
    B_commit: Commitment = field(init=False)
    D_commit: Commitment = field(init=False)
    Y_commit: Commitment = field(init=False)
    W_commit: Commitment = field(init=False)
    K_commit: Commitment = field(init=False)
    right: Commitment = field(init=False)
    left: Commitment = field(init=False)
    Q: Element = field(init=False)

    def __post_init__(self) -> None:
        # if upper bound is not set then it becomes field prime minus one
        if self.upper_bound is None:
            self.upper_bound = field_order - 1
        # upper bound cant be larger than the field prime
        if self.upper_bound > field_order - 1:
            raise ValueError(
                "Invalid Range Proof: Upper bound must be less than field order."
            )

        # if the lower bound is not set it becomes zero
        if self.lower_bound is None:
            self.lower_bound = 0
        # lower bound can't be smaller than zero
        if self.lower_bound < 0:
            raise ValueError(
                "Invalid Range Proof: Lower bound must be greater than or equal to zero."
            )

        # Set up D commitment
        self.D_commit = Commitment(self.secret_value)

        # Set up Y commitment
        y = self.upper_bound - self.secret_value
        if y < 0:
            raise ValueError(
                "Invalid Range Proof: Y value must be greater than or equal to zero."
            )
        self.Y_commit = Commitment(y)

        # Set up W commitment
        w = self.secret_value - self.lower_bound
        if w < 0:
            raise ValueError(
                "Invalid Range Proof: W value must be greater than or equal to zero."
            )
        self.W_commit = Commitment(w)

        # Set up A and B commitments with public randomness
        self.A_commit = Commitment(self.upper_bound)
        self.B_commit = Commitment(self.lower_bound)

        # Set up Q
        self.Q = Element(g2_point(1))

        # need to account for the random r values
        self.right = Commitment(0, self.A_commit.r + self.B_commit.r + self.W_commit.r)
        self.left = Commitment(0, self.Y_commit.r + self.D_commit.r + self.D_commit.r)

    def __str__(self) -> str:
        return f"Range(\nY={self.Y_commit.c},\n{(self.D_commit + self.D_commit).c},\nR={self.right.c},\nW={self.W_commit.c},\nL={self.left.c}\n)"

    def schnorr(self, z_a, a_c, flag) -> bool:
        if flag is True:
            r_commitment = self.A_commit - Commitment(self.upper_bound, 0)
        else:
            r_commitment = self.B_commit - Commitment(self.lower_bound, 0)
        beta = generate(a_c + r_commitment.c.value)
        b = int(beta, 16)
        z_commitment = Commitment(0, z_a)
        right = Element(a_c) + (b * r_commitment.c)
        return z_commitment.c.value == right.value

    def prove(self, z_a, a_c, z_b, b_c) -> bool:
        # prove they know the r in A_commit
        check_a = self.schnorr(z_a, a_c, True)
        # prove they know the r in B_commit
        check_b = self.schnorr(z_b, b_c, False)
        # prove the pairing range proof
        left_pair = pair(
            self.Q.value,
            ((self.Y_commit + self.D_commit + self.D_commit).c + self.right.c).value,
        )
        right_pair = pair(
            self.Q.value,
            (self.A_commit.c + self.B_commit.c + self.W_commit.c + self.left.c).value,
        )
        check_p = left_pair == right_pair
        # Verifying that the commitments are consistent with the expected range proof
        return check_p and check_a and check_b

    def generate_proof(self) -> dict:
        # do the schnorr proofs
        r_upper_commitment = self.A_commit - Commitment(self.upper_bound, 0)
        r_lower_commitment = self.B_commit - Commitment(self.lower_bound, 0)

        alpha = rng()
        alpha_upper_commitment = Commitment(0, alpha)
        beta = fiat_shamir_heuristic(
            Commitment(0, 1).c.value,
            alpha_upper_commitment.c.value,
            r_upper_commitment.c.value,
        )
        b = int(beta, 16)
        z_a = (alpha + b * self.A_commit.r) % field_order
        a_c = alpha_upper_commitment.c.value

        alpha = rng()
        alpha_lower_commitment = Commitment(0, alpha)
        beta = fiat_shamir_heuristic(
            Commitment(0, 1).c.value,
            alpha_lower_commitment.c.value,
            r_lower_commitment.c.value,
        )
        b = int(beta, 16)
        z_b = (alpha + b * self.B_commit.r) % field_order
        b_c = alpha_lower_commitment.c.value

        data = {
            "Y": self.Y_commit.c.value,
            "D": (self.D_commit + self.D_commit).c.value,
            "R": self.right.c.value,
            "W": self.W_commit.c.value,
            "L": self.left.c.value,
            "A": self.A_commit.c.value,
            "B": self.B_commit.c.value,
            "Za": hexify(z_a),
            "ac": a_c,
            "Zb": hexify(z_b),
            "bc": b_c,
        }
        return data

    @staticmethod
    def verify_proof(proof, lower_bound, upper_bound) -> bool:
        #
        # Verify A
        #
        r_upper_commitment = Element(proof["A"]) + Element(
            invert(Commitment(upper_bound, 0).c.value)
        )
        beta = fiat_shamir_heuristic(
            Commitment(0, 1).c.value, proof["ac"], r_upper_commitment.value
        )
        b = int(beta, 16)
        z_commitment = Commitment(0, int(proof["Za"], 16))
        right = Element(proof["ac"]) + (b * r_upper_commitment)
        check_a = z_commitment.c.value == right.value
        #
        # Verify B
        #
        r_lower_commitment = Element(proof["B"]) + Element(
            invert(Commitment(lower_bound, 0).c.value)
        )
        beta = fiat_shamir_heuristic(
            Commitment(0, 1).c.value, proof["bc"], r_lower_commitment.value
        )
        b = int(beta, 16)
        z_commitment = Commitment(0, int(proof["Zb"], 16))
        right = Element(proof["bc"]) + (b * r_lower_commitment)
        check_b = z_commitment.c.value == right.value
        #
        # Verify Pairing
        #
        Q = Element(g2_point(1))
        left_pair = pair(
            Q.value,
            (Element(proof["Y"]) + Element(proof["D"]) + Element(proof["R"])).value,
        )
        right_pair = pair(
            Q.value,
            (
                Element(proof["A"])
                + Element(proof["B"])
                + Element(proof["W"])
                + Element(proof["L"])
            ).value,
        )
        check_p = left_pair == right_pair
        # Verifying that the commitments are consistent with the expected range proof
        return check_a and check_b and check_p
