use rs::range::prove;
use rs::pedersen::commitment;
use rs::constants::decompress;
use blstrs::G1Projective;

#[test]
fn test_commitment_based_proof() {
    let a: u64 = 10;
    let b: u64 = 0;
    let d: u64 = 7;

    let y: G1Projective = commitment(a - d, 1);
    let d_point: G1Projective = commitment(d, 1) + commitment(d, 1);
    let p: G1Projective = commitment(0, 3);
    let a_point: G1Projective = commitment(a, 1);
    let b_point: G1Projective = commitment(b, 1);
    let w: G1Projective = commitment(d - b, 1);
    let l: G1Projective = commitment(0, 3);

    assert!(prove(y, d_point, p, a_point, b_point, w, l));
}

#[test]
fn test_simple_range_proof() {
      let y: G1Projective = decompress("84ea78e4c3a283c5e8c178f1ff9e384abb11ff93888b4bc8eb4297131dceec0db2c528015303323309137994e4550bbf");
      let d: G1Projective = decompress("8e905fa2a944570cdd5933334394c0b937582169d555c90ad158b63304d3d89c96c822bb489dc82d7eca01cf7daaf92f");
      let p: G1Projective = decompress("8109eba987d1692ba22195d87507d4405a8598701844987c7bdcd634b069aabd4b50663bd0f4d9411169ee65d1950b23");
      let a: G1Projective = decompress("8d8a58fed45ab8b1e48deb07561070c7eef4e712fbfeeb1d82d041f1c2dfc4a6e52feeea10432bcd4e60017f45102e9a");
      let b: G1Projective = decompress("81d43f697a75ad20a807c9b7446846dbc7f4f7cac6ecb212632eaff2c55e94cd42c906300d663375903e1e1d5efbfbe7");
      let w: G1Projective = decompress("b145b1b4465e85cd79af4f957449b2e2b7266716decdcc92f3613425d29f1d18cb3e93ba3b3cec801645f781ab794bdc");
      let l: G1Projective = decompress("b72f1c1b1a9726c20579963fa60bb699701d71f4c0a854748e8b630457a9948c33092d41b9a2e70091ddf7dd580b2edc");
    assert!(prove(y, d, p, a, b, w, l));
}