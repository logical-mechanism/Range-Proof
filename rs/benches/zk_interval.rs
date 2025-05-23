// benches/zk_interval.rs
//
// 64-bit
// prover time: 2.201 milliseconds
// verifier time: 1.5497 milliseconds
//

use blstrs::Scalar;
use criterion::{Criterion, criterion_group, criterion_main};
// use ff::Field;
use rs::constants::sk_to_g1;
use rs::range::{create_range_proof, prove_range};
use rs::schnorr::{create_schnorr_proof, prove_schnorr};
// use rs::schnorr::random_scalar;

fn bench_all(c: &mut Criterion) {
    // common inputs
    let generator = "97F1D3A73197D7942695638C4FA9AC0FC3688C4F9774B905A14E3A3F171BAC586C55E83FF97A1AEFFB3AF00ADB22C6BB";
    // let a: Scalar = -Scalar::ONE;
    let a: Scalar = Scalar::from(18446744073709551615);
    let b: Scalar = Scalar::from(0);
    // let d: Scalar = random_scalar();
    let d: Scalar = Scalar::from(4398046511119);

    // generate one range proof to get its nonces & commitments
    let (y, dpt, p, apt, bpt, w, l, ar, br) = create_range_proof(a, b, d);

    // build Schnorr inputs
    let ak: Scalar = Scalar::from(ar);
    let ak_pub: String = sk_to_g1(generator, ak);
    let (z_a, g_r_a) = create_schnorr_proof(generator.to_string(), ak_pub.clone(), ak);

    let bk: Scalar = Scalar::from(br);
    let bk_pub: String = sk_to_g1(generator, bk);
    let (z_b, g_r_b) = create_schnorr_proof(generator.to_string(), bk_pub.clone(), bk);

    let ak_pub_verify = ak_pub.clone();
    let bk_pub_verify = bk_pub.clone();
    // list of (benchmark name, closure) pairs
    let benches: Vec<(&str, Box<dyn Fn() + 'static>)> = vec![
        (
            "range_proof_gen",
            Box::new(move || {
                let _ = create_range_proof(a, b, d);
            }),
        ),
        (
            "schnorr_proof_gen_ak",
            Box::new(move || {
                let _ = create_schnorr_proof(generator.to_string(), ak_pub.clone(), ak);
            }),
        ),
        (
            "schnorr_proof_gen_bk",
            Box::new(move || {
                let _ = create_schnorr_proof(generator.to_string(), bk_pub.clone(), bk);
            }),
        ),
        (
            "range_proof_verify",
            Box::new(move || {
                assert!(prove_range(y, dpt, p, apt, bpt, w, l));
            }),
        ),
        (
            "schnorr_proof_verify_ak",
            Box::new(move || {
                assert!(prove_schnorr(generator, &ak_pub_verify, &z_a, &g_r_a));
            }),
        ),
        (
            "schnorr_proof_verify_bk",
            Box::new(move || {
                assert!(prove_schnorr(generator, &bk_pub_verify, &z_b, &g_r_b));
            }),
        ),
    ];

    // register each as its own benchmark
    for (name, func) in benches {
        c.bench_function(name, |b| b.iter(|| func()));
    }
}

criterion_group!(zk_interval_benches, bench_all);
criterion_main!(zk_interval_benches);
