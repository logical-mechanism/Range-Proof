use aiken/crypto/bls12_381/g1
use aiken/crypto/bls12_381/scalar.{Scalar}
use constants.{g, h}

pub fn commitment(vi: Int, ri: Int) -> G1Element {
  expect Some(v): Option<Scalar> = scalar.new(vi)
  expect Some(r): Option<Scalar> = scalar.new(ri)
  g1.scale(h, v) |> g1.add(g1.scale(g, r))
}

test commit_to_zero() {
  commitment(0, 0) == g1.zero
}

test commit_to_generator() {
  commitment(0, 1) == g
}

test commit_to_square() {
  commitment(0, 2) == h
}

test can_not_do_negative() fail {
  commitment(0, -2) == g
}

test simple_addition() {
  g1.add(commitment(1, 2), commitment(2, 1)) == commitment(3, 3)
}
