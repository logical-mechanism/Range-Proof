use blstrs::Scalar;
use rs::constants::sk_to_g1;
use rs::schnorr::{create_schnorr_proof, fiat_shamir_heuristic, prove_schnorr, random_scalar};

#[test]
fn test_empty_fiat_shamir_heuristic() {
    assert_eq!(
        fiat_shamir_heuristic("".to_string(), "".to_string(), "".to_string()),
        "836cc68931c2e4e3e838602eca1902591d216837bafddfe6f0c8cb07"
    )
}

#[test]
fn test_real_fiat_shamir_heuristic() {
    assert_eq!(fiat_shamir_heuristic(
    "86f0c64bd433568dd92751f0bee97feaaeee6f3c2144b210be68d2bc85253b1994703caf7f8361ccf246fef52c0ad859".to_string(),
    "97f1d3a73197d7942695638c4fa9ac0fc3688c4f9774b905a14e3a3f171bac586c55e83ff97a1aeffb3af00adb22c6bb".to_string(),
    "a2cbc5c3c72a7bc9047971345df392a67279d2f32082891976d913c699885c3ff9a90a8ea942bef4729cf93f526521e4".to_string(),
  ), "c4f2937e8317aee04a17b6ea65b2e3706aabd75dd2ebce5e6c8744ed")
}

#[test]
fn valid_schnorr_proof() {
    let generator = "97F1D3A73197D7942695638C4FA9AC0FC3688C4F9774B905A14E3A3F171BAC586C55E83FF97A1AEFFB3AF00ADB22C6BB";
    let sk = random_scalar();
    let public_value = sk_to_g1(generator, sk);
    let (z_b, g_r_b) = create_schnorr_proof(generator.to_string(), public_value.clone(), sk);
    assert!(prove_schnorr(generator, &public_value, &z_b, &g_r_b))
}

#[test]
fn valid_endpoint_proof() {
    let generator = "97F1D3A73197D7942695638C4FA9AC0FC3688C4F9774B905A14E3A3F171BAC586C55E83FF97A1AEFFB3AF00ADB22C6BB";
    let sk = Scalar::from(0u64);
    let public_value = sk_to_g1(generator, sk);
    let (z_b, g_r_b) = create_schnorr_proof(generator.to_string(), public_value.clone(), sk);
    assert!(prove_schnorr(generator, &public_value, &z_b, &g_r_b))
}
