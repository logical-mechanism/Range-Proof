use blstrs::{G1Projective, Scalar};
use crate::constants::{g, h};

/// Create a Pedersen-style commitment: h^v * g^r
pub fn commitment(vi: u64, ri: u64) -> G1Projective {
    let v: Scalar = Scalar::from(vi);
    let r: Scalar = Scalar::from(ri);

    h() * v + g() * r
}
