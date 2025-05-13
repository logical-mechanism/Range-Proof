use blstrs:: {G1Projective, G2Affine};
use blstrs::pairing;
use crate::constants::q;
use group::Curve;

/// Performs the pairing check:
/// e(Q, y + d + p) == e(Q, a + b + w + l)
///
/// Returns true if the proof is valid.
pub fn prove(
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
