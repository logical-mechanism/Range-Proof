import json
from random import randrange

import pytest
from src.blake2b_224 import generate
from src.bls12_381 import field_order, rng
from src.commitment import Commitment
from src.range import Range


def test_valid_range():
    upper = field_order - 1
    lower = 1
    value = randrange(lower, upper)
    r = Range(secret_value=value, lower_bound=lower, upper_bound=upper)

    # do the schnorr proofs
    r_upper_commitment = r.A_commit - Commitment(upper, 0)
    r_lower_commitment = r.B_commit - Commitment(lower, 0)

    alpha = rng()
    alpha_upper_commitment = Commitment(0, alpha)

    beta = generate(alpha_upper_commitment.c.value + r_upper_commitment.c.value)
    b = int(beta, 16)
    z_a = (alpha + b * r.A_commit.r) % field_order
    a_c = alpha_upper_commitment.c.value

    alpha = rng()
    alpha_lower_commitment = Commitment(0, alpha)
    beta = generate(alpha_lower_commitment.c.value + r_lower_commitment.c.value)
    b = int(beta, 16)
    z_b = (alpha + b * r.B_commit.r) % field_order
    b_c = alpha_lower_commitment.c.value

    assert r.prove(z_a, a_c, z_b, b_c)


def test_64_bit_range():
    lower = 0
    upper = pow(2, 64)
    value = randrange(lower, upper)
    r = Range(secret_value=value, lower_bound=lower, upper_bound=upper)
    # do the schnorr proofs
    r_upper_commitment = r.A_commit - Commitment(upper, 0)
    r_lower_commitment = r.B_commit - Commitment(lower, 0)

    alpha = rng()
    alpha_upper_commitment = Commitment(0, alpha)

    beta = generate(alpha_upper_commitment.c.value + r_upper_commitment.c.value)
    b = int(beta, 16)
    z_a = (alpha + b * r.A_commit.r) % field_order
    a_c = alpha_upper_commitment.c.value

    alpha = rng()
    alpha_lower_commitment = Commitment(0, alpha)
    beta = generate(alpha_lower_commitment.c.value + r_lower_commitment.c.value)
    b = int(beta, 16)
    z_b = (alpha + b * r.B_commit.r) % field_order
    b_c = alpha_lower_commitment.c.value

    assert r.prove(z_a, a_c, z_b, b_c)


def test_age_verification_model_too_low():
    lower = 18
    upper = 25
    age = 17
    with pytest.raises(
        ValueError,
        match="Invalid Range Proof: W value must be greater than or equal to zero.",
    ):
        Range(secret_value=age, lower_bound=lower, upper_bound=upper)


def test_age_verification_model_too_high():
    lower = 18
    upper = 25
    age = 32
    with pytest.raises(
        ValueError,
        match="Invalid Range Proof: Y value must be greater than or equal to zero.",
    ):
        Range(secret_value=age, lower_bound=lower, upper_bound=upper)


def test_age_verification_model1():
    lower = 18
    upper = 25
    age = 21
    r = Range(secret_value=age, lower_bound=lower, upper_bound=upper)

    # do the schnorr proofs
    r_upper_commitment = r.A_commit - Commitment(upper, 0)
    r_lower_commitment = r.B_commit - Commitment(lower, 0)

    alpha = rng()
    alpha_upper_commitment = Commitment(0, alpha)

    beta = generate(alpha_upper_commitment.c.value + r_upper_commitment.c.value)
    b = int(beta, 16)
    z_a = (alpha + b * r.A_commit.r) % field_order
    a_c = alpha_upper_commitment.c.value

    alpha = rng()
    alpha_lower_commitment = Commitment(0, alpha)
    beta = generate(alpha_lower_commitment.c.value + r_lower_commitment.c.value)
    b = int(beta, 16)
    z_b = (alpha + b * r.B_commit.r) % field_order
    b_c = alpha_lower_commitment.c.value

    assert r.prove(z_a, a_c, z_b, b_c)


def test_age_verification_model2():
    lower = 20
    upper = 125  # oldest ever is 122
    age = 21
    r = Range(secret_value=age, lower_bound=lower, upper_bound=upper)

    # do the schnorr proofs
    r_upper_commitment = r.A_commit - Commitment(upper, 0)
    r_lower_commitment = r.B_commit - Commitment(lower, 0)

    alpha = rng()
    alpha_upper_commitment = Commitment(0, alpha)

    beta = generate(alpha_upper_commitment.c.value + r_upper_commitment.c.value)
    b = int(beta, 16)
    z_a = (alpha + b * r.A_commit.r) % field_order
    a_c = alpha_upper_commitment.c.value

    alpha = rng()
    alpha_lower_commitment = Commitment(0, alpha)
    beta = generate(alpha_lower_commitment.c.value + r_lower_commitment.c.value)
    b = int(beta, 16)
    z_b = (alpha + b * r.B_commit.r) % field_order
    b_c = alpha_lower_commitment.c.value

    assert r.prove(z_a, a_c, z_b, b_c)


def test_lower_range_value():
    lower = 0
    upper = 125  # oldest ever is 122
    age = 0
    r = Range(secret_value=age, lower_bound=lower, upper_bound=upper)

    # do the schnorr proofs
    r_upper_commitment = r.A_commit - Commitment(upper, 0)
    r_lower_commitment = r.B_commit - Commitment(lower, 0)

    alpha = rng()
    alpha_upper_commitment = Commitment(0, alpha)

    beta = generate(alpha_upper_commitment.c.value + r_upper_commitment.c.value)
    b = int(beta, 16)
    z_a = (alpha + b * r.A_commit.r) % field_order
    a_c = alpha_upper_commitment.c.value

    alpha = rng()
    alpha_lower_commitment = Commitment(0, alpha)
    beta = generate(alpha_lower_commitment.c.value + r_lower_commitment.c.value)
    b = int(beta, 16)
    z_b = (alpha + b * r.B_commit.r) % field_order
    b_c = alpha_lower_commitment.c.value

    assert r.prove(z_a, a_c, z_b, b_c)


def test_null_range_value():
    lower = 0
    upper = 0
    age = 0
    r = Range(secret_value=age, lower_bound=lower, upper_bound=upper)

    # do the schnorr proofs
    r_upper_commitment = r.A_commit - Commitment(upper, 0)
    r_lower_commitment = r.B_commit - Commitment(lower, 0)

    alpha = rng()
    alpha_upper_commitment = Commitment(0, alpha)

    beta = generate(alpha_upper_commitment.c.value + r_upper_commitment.c.value)
    b = int(beta, 16)
    z_a = (alpha + b * r.A_commit.r) % field_order
    a_c = alpha_upper_commitment.c.value

    alpha = rng()
    alpha_lower_commitment = Commitment(0, alpha)
    beta = generate(alpha_lower_commitment.c.value + r_lower_commitment.c.value)
    b = int(beta, 16)
    z_b = (alpha + b * r.B_commit.r) % field_order
    b_c = alpha_lower_commitment.c.value

    assert r.prove(z_a, a_c, z_b, b_c)


def test_upper_range_value():
    with pytest.raises(
        ValueError,
        match="Invalid Range Proof: Y value must be greater than or equal to zero.",
    ):
        Range(field_order)


def test_prove_knowledge():
    upper_bound = field_order - 1
    d = randrange(1, upper_bound)
    r = Range(d)
    r_commitment = r.A_commit - Commitment(upper_bound, 0)

    alpha = randrange(1, field_order - 1)
    alpha_commitment = Commitment(0, alpha)

    beta = generate(alpha_commitment.c.value + r_commitment.c.value)
    b = int(beta, 16)
    z = alpha + b * r.A_commit.r
    z = (alpha + b * r.A_commit.r) % field_order

    assert r.schnorr(z, alpha_commitment.c.value, True)


def test_proof_generation1():
    lower = 20
    upper = 125  # oldest ever is 122
    age = 21
    r = Range(secret_value=age, lower_bound=lower, upper_bound=upper)
    proof = r.generate_proof()
    print(f"Proof:\n{json.dumps(proof, indent=4, sort_keys=True, default=str)}")
    combined_string = "".join(f"{key}:{value} " for key, value in proof.items()).strip()
    print(f"Approximately: {len(combined_string) // 2} Bytes")
    assert Range.verify_proof(proof, lower, upper)


def test_proof_generation2():
    lower = 0
    upper = pow(2, 64) - 1
    age = randrange(lower, upper)
    r = Range(secret_value=age, lower_bound=lower, upper_bound=upper)
    proof = r.generate_proof()
    print(f"Proof:\n{json.dumps(proof, indent=4, sort_keys=True, default=str)}")
    combined_string = "".join(f"{key}:{value} " for key, value in proof.items()).strip()
    print(f"Approximately: {len(combined_string) // 2} Bytes")
    assert Range.verify_proof(proof, lower, upper)

def test_proof_generation3():
    lower = 0
    upper = pow(2, 64) - 1
    age = randrange(lower, upper)
    r = Range(secret_value=age, lower_bound=lower, upper_bound=upper)
    r.generate_proof()

if __name__ == "__main__":
    pytest.main()
