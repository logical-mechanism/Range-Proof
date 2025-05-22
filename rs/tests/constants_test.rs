use blstrs::{G1Projective, G2Projective, Scalar};
use rs::constants::*;

#[test]
fn create_g() {
    let g_proj: G1Projective = g();
    let one: Scalar = Scalar::from(1u64);
    assert_eq!(g_proj * one, g_proj);
}

#[test]
fn add_g_to_g() {
    let g_proj: G1Projective = g();
    let h_proj: G1Projective = h();
    assert_eq!(g_proj + g_proj, h_proj);
}

#[test]
fn create_h_from_g() {
    let g_proj: G1Projective = g();
    let two: Scalar = Scalar::from(2u64);
    let expected: G1Projective = g_proj * two;
    assert_eq!(expected, h());
}

#[test]
fn create_q() {
    let q_proj: G2Projective = q();
    let one: Scalar = Scalar::from(1u64);
    assert_eq!(q_proj * one, q_proj);
}
