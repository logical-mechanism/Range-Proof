use blstrs::G1Projective;
use rs::{pedersen::commitment, constants::{g, h}};
use group::Group;

#[test]
fn commit_to_zero() {
    let c: G1Projective = commitment(0, 0);
    assert_eq!(c, G1Projective::identity());
}


#[test]
fn commit_to_generator() {
    let c: G1Projective = commitment(0, 1);
    assert_eq!(c, g());
}

#[test]
fn commit_to_square() {
    let c: G1Projective = commitment(0, 2);
    assert_eq!(c, h());
}


#[test]
fn simple_addition() {
    let a: G1Projective = commitment(1, 2);
    let b: G1Projective = commitment(2, 1);
    let expected: G1Projective = commitment(3, 3);

    assert_eq!(a + b, expected);
}