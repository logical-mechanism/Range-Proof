use blstrs::{G1Projective, Scalar};
use group::Group;
use rs::{
    constants::{g, h},
    pedersen::commitment,
};

#[test]
fn commit_to_zero() {
    let c: G1Projective = commitment(Scalar::from(0), Scalar::from(0));
    assert_eq!(c, G1Projective::identity());
}

#[test]
fn commit_to_generator() {
    let c: G1Projective = commitment(Scalar::from(0), Scalar::from(1));
    assert_eq!(c, g());
}

#[test]
fn commit_to_square() {
    let c: G1Projective = commitment(Scalar::from(0), Scalar::from(2));
    assert_eq!(c, h());
}

#[test]
fn simple_addition() {
    let a: G1Projective = commitment(Scalar::from(1), Scalar::from(2));
    let b: G1Projective = commitment(Scalar::from(2), Scalar::from(1));
    let expected: G1Projective = commitment(Scalar::from(3), Scalar::from(3));

    assert_eq!(a + b, expected);
}
