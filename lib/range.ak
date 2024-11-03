use aiken/builtin
use aiken/crypto/bls12_381/g1
use aiken/crypto/bls12_381/g2
use constants.{q, qi}
use pedersen.{commitment}

// These are the compressed g1 elements in the weil pairing
//
// e(Q, Y + D + P) * e(-Q, A + B + W + L) == 1
//
// see paper for details
pub type RangeProof {
  yb: ByteArray,
  db: ByteArray,
  pb: ByteArray,
  ab: ByteArray,
  bb: ByteArray,
  wb: ByteArray,
  lb: ByteArray,
}

pub fn prove(rp: RangeProof) -> Bool {
  //
  // decompress the elements
  let y: G1Element = g1.decompress(rp.yb)
  let d: G1Element = g1.decompress(rp.db)
  let p: G1Element = g1.decompress(rp.pb)
  let a: G1Element = g1.decompress(rp.ab)
  let b: G1Element = g1.decompress(rp.bb)
  let w: G1Element = g1.decompress(rp.wb)
  let l: G1Element = g1.decompress(rp.lb)
  //
  // add up the points
  let left: G1Element = y |> g1.add(d) |> g1.add(p)
  let right: G1Element = a |> g1.add(b) |> g1.add(w) |> g1.add(l)
  //
  // create the weil pairings
  let positive: MillerLoopResult = builtin.bls12_381_miller_loop(left, q)
  let negative: MillerLoopResult = builtin.bls12_381_miller_loop(right, qi)
  //
  // the multiplication of the negative and positive must be the loop of zero
  builtin.bls12_381_final_verify(
    builtin.bls12_381_mul_miller_loop_result(positive, negative),
    builtin.bls12_381_miller_loop(g1.zero, g2.zero),
  )
}

test simple_range_proof() {
  let rp: RangeProof =
    RangeProof {
      yb: #"84ea78e4c3a283c5e8c178f1ff9e384abb11ff93888b4bc8eb4297131dceec0db2c528015303323309137994e4550bbf",
      db: #"8e905fa2a944570cdd5933334394c0b937582169d555c90ad158b63304d3d89c96c822bb489dc82d7eca01cf7daaf92f",
      pb: #"8109eba987d1692ba22195d87507d4405a8598701844987c7bdcd634b069aabd4b50663bd0f4d9411169ee65d1950b23",
      ab: #"8d8a58fed45ab8b1e48deb07561070c7eef4e712fbfeeb1d82d041f1c2dfc4a6e52feeea10432bcd4e60017f45102e9a",
      bb: #"81d43f697a75ad20a807c9b7446846dbc7f4f7cac6ecb212632eaff2c55e94cd42c906300d663375903e1e1d5efbfbe7",
      wb: #"b145b1b4465e85cd79af4f957449b2e2b7266716decdcc92f3613425d29f1d18cb3e93ba3b3cec801645f781ab794bdc",
      lb: #"b72f1c1b1a9726c20579963fa60bb699701d71f4c0a854748e8b630457a9948c33092d41b9a2e70091ddf7dd580b2edc",
    }
  prove(rp)
}

test build_simple_range_proof() {
  let a: Int = 10
  let b: Int = 0
  let d: Int = 7
  let rp: RangeProof =
    RangeProof {
      yb: commitment(a - d, 1) |> g1.compress,
      db: g1.add(commitment(d, 1), commitment(d, 1)) |> g1.compress,
      pb: commitment(0, 3) |> g1.compress,
      ab: commitment(a, 1) |> g1.compress,
      bb: commitment(b, 1) |> g1.compress,
      wb: commitment(d - b, 1) |> g1.compress,
      lb: commitment(0, 3) |> g1.compress,
    }
  prove(rp)
}
