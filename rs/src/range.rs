use crate::constants::q;
use crate::pedersen::commitment;
use crate::schnorr::random_scalar;
use blstrs::pairing;
use blstrs::{G1Projective, G2Affine, Scalar};
use group::Curve;

pub fn create_range_proof(
    a: Scalar,
    b: Scalar,
    d: Scalar,
) -> (
    G1Projective,
    G1Projective,
    G1Projective,
    G1Projective,
    G1Projective,
    G1Projective,
    G1Projective,
    Scalar,
    Scalar,
) {
    let yr: Scalar = random_scalar();
    let dr1: Scalar = random_scalar();
    let dr2: Scalar = random_scalar();

    let y: G1Projective = commitment(a - d, yr);
    let d_point: G1Projective = commitment(d, dr1) + commitment(d, dr2);

    let ar: Scalar = random_scalar();
    let br: Scalar = random_scalar();
    let wr: Scalar = random_scalar();

    let a_point: G1Projective = commitment(a, ar);
    let b_point: G1Projective = commitment(b, br);
    let w: G1Projective = commitment(d - b, wr);

    let p: G1Projective = commitment(Scalar::from(0), ar + br + wr);
    let l: G1Projective = commitment(Scalar::from(0), yr + dr1 + dr2);

    (y, d_point, p, a_point, b_point, w, l, ar, br)
}

/// Performs the pairing check:
/// e(Q, y + d + p) == e(Q, a + b + w + l)
///
/// Returns true if the proof is valid.
pub fn prove_range(
    y: G1Projective,
    d: G1Projective,
    p: G1Projective,
    a: G1Projective,
    b: G1Projective,
    w: G1Projective,
    l: G1Projective,
) -> bool {
    let q_affine: G2Affine = G2Affine::from(q());

    let left: G1Projective = y + d + p;
    let right: G1Projective = a + b + w + l;

    pairing(&left.to_affine(), &q_affine) == pairing(&right.to_affine(), &q_affine)
}
