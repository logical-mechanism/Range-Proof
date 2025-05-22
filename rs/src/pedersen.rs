use crate::constants::{g, h};
use blstrs::{G1Projective, Scalar};

/// Create a Pedersen-style commitment: h^v * g^r
pub fn commitment(v: Scalar, r: Scalar) -> G1Projective {
    h() * v + g() * r
}
