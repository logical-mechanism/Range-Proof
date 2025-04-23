use aiken/crypto
use aiken/crypto/bls12_381/g1
use aiken/crypto/bls12_381/scalar.{Scalar}
use aiken/primitive/bytearray
use constants.{g}

pub type SchnorrProof {
  // this is z = r + c * x as a bytearray
  z_b: ByteArray,
  // this is the g^r compressed G1Element
  g_r_b: ByteArray,
}

test empty_string_hash() {
  crypto.blake2b_224(#"") == #"836cc68931c2e4e3e838602eca1902591d216837bafddfe6f0c8cb07"
}

test hello_world_hash() {
  crypto.blake2b_224("Hello, world!") == #"e552ae1ccaacf44a0e1939b2f85fe39b9eb9f5fa6abb41560716dec1"
}

pub fn fiat_shamir_heuristic(
  // compressed g element
  g_b: ByteArray,
  // compressed g^r element
  g_r_b: ByteArray,
  // compressed g^x element
  u_b: ByteArray,
) -> ByteArray {
  g_b
    |> bytearray.concat(g_r_b)
    |> bytearray.concat(u_b)
    |> crypto.blake2b_224()
}

test empty_fiat_shamir_heuristic() {
  fiat_shamir_heuristic(#"", #"", #"") == #"836cc68931c2e4e3e838602eca1902591d216837bafddfe6f0c8cb07"
}

test real_fiat_shamir_heuristic() {
  fiat_shamir_heuristic(
    #"86f0c64bd433568dd92751f0bee97feaaeee6f3c2144b210be68d2bc85253b1994703caf7f8361ccf246fef52c0ad859",
    #"97f1d3a73197d7942695638c4fa9ac0fc3688c4f9774b905a14e3a3f171bac586c55e83ff97a1aeffb3af00adb22c6bb",
    #"a2cbc5c3c72a7bc9047971345df392a67279d2f32082891976d913c699885c3ff9a90a8ea942bef4729cf93f526521e4",
  ) == #"c4f2937e8317aee04a17b6ea65b2e3706aabd75dd2ebce5e6c8744ed"
}

pub fn prove(sp: SchnorrProof, value: ByteArray) -> Bool {
  //
  // the z computation: g^z = g^(r + c * x) 
  //                        = g^r * g^(c * x)
  //                        = g^r * (g^x)^c
  //                        = g^r * u^c
  expect Some(z): Option<Scalar> = scalar.from_bytearray_big_endian(sp.z_b)
  let g_z: G1Element = g1.scale(g, z)
  //
  // use the fiat-shamir heuristic to calculate the challenge then convert it to an integer
  expect Some(c): Option<Scalar> =
    fiat_shamir_heuristic(g1.compress(g), sp.g_r_b, value)
      |> scalar.from_bytearray_big_endian()
  //
  // the u^c computation: u^c = (g^x)^c = g^(x * c)
  let u_c: G1Element = g1.decompress(value) |> g1.scale(c)
  //
  // check if the equation: g^z = g^r * u^c is true
  //
  g_z |> g1.equal(g1.add(g1.decompress(sp.g_r_b), u_c))
}

test a_simple_proof() {
  expect Some(x): Option<Scalar> = scalar.new(123)
  expect Some(r): Option<Scalar> = scalar.new(321)
  let value: G1Element = g1.scale(g, x)
  let g_r_b: ByteArray = g1.scale(g, r) |> g1.compress
  // use the fiat-shamir heuristic to calculate the challenge then convert it to an integer
  expect Some(c): Option<Scalar> =
    fiat_shamir_heuristic(g |> g1.compress, g_r_b, value |> g1.compress)
      |> scalar.from_bytearray_big_endian()
  let z: Scalar = scalar.add(r, scalar.mul(x, c))
  let sp: SchnorrProof =
    SchnorrProof {
      // this is z = r + c * x as a bytearray
      z_b: scalar.to_bytearray_big_endian(z, 0),
      // this is the g^r compressed G1Element
      g_r_b,
    }
  prove(sp, value |> g1.compress)
}

test a_schnorr_proof() {
  expect Some(x): Option<Scalar> =
    scalar.new(
      2036760191456846364146524130282210542527356522269466450157845405735892,
    )
  expect Some(r): Option<Scalar> =
    scalar.new(
      16559025946803628976801009189286264573393142457475336993153214680777,
    )
  let value: G1Element = g1.scale(g, x)
  let g_r_b: ByteArray = g1.scale(g, r) |> g1.compress
  // use the fiat-shamir heuristic to calculate the challenge then convert it to an integer
  expect Some(c): Option<Scalar> =
    fiat_shamir_heuristic(g |> g1.compress, g_r_b, value |> g1.compress)
      |> scalar.from_bytearray_big_endian()
  let z: Scalar = scalar.add(r, scalar.mul(x, c))
  let sp: SchnorrProof =
    SchnorrProof {
      // this is z = r + c * x as a bytearray
      z_b: scalar.to_bytearray_big_endian(z, 0),
      // this is the g^r compressed G1Element
      g_r_b,
    }
  prove(sp, value |> g1.compress)
}
