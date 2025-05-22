use blstrs::Scalar;
use ff::Field;
use rs::constants::sk_to_g1;
use rs::range::{create_range_proof, prove_range};
use rs::schnorr::{create_schnorr_proof, prove_schnorr, random_scalar};

#[test]
fn valid_zk_interval_proof() {
    let generator: &'static str = "97F1D3A73197D7942695638C4FA9AC0FC3688C4F9774B905A14E3A3F171BAC586C55E83FF97A1AEFFB3AF00ADB22C6BB";

    let a: Scalar = -Scalar::ONE;
    let b: Scalar = Scalar::from(0);
    let d: Scalar = random_scalar();

    let (y, d_point, p, a_point, b_point, w, l, ar, br) = create_range_proof(a, b, d);

    let ak: Scalar = Scalar::from(ar);
    let ak_public_value: String = sk_to_g1(generator, ak);
    let (z_a, g_r_a) = create_schnorr_proof(generator.to_string(), ak_public_value.clone(), ak);

    let bk: Scalar = Scalar::from(br);
    let bk_public_value: String = sk_to_g1(generator, bk);
    let (z_b, g_r_b) = create_schnorr_proof(generator.to_string(), bk_public_value.clone(), bk);

    assert!(prove_range(y, d_point, p, a_point, b_point, w, l));
    assert!(prove_schnorr(generator, &ak_public_value, &z_a, &g_r_a));
    assert!(prove_schnorr(generator, &bk_public_value, &z_b, &g_r_b));
}
