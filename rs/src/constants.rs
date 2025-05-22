use blstrs::{G1Affine, G1Projective, G2Affine, G2Projective, Scalar};
use group::Curve;

/// g^1 (in G1)
pub const G_BYTES: [u8; 48] = hex_literal::hex!(
    "97f1d3a73197d7942695638c4fa9ac0fc3688c4f9774b905a14e3a3f171bac586c55e83ff97a1aeffb3af00adb22c6bb"
);

/// g^2 (in G1, g * 2)
pub const H_BYTES: [u8; 48] = hex_literal::hex!(
    "a572cbea904d67468808c8eb50a9450c9721db309128012543902d0ac358a62ae28f75bb8f1c7c42c39a8c5529bf0f4e"
);

/// q^1 (in G2)
pub const Q_BYTES: [u8; 96] = hex_literal::hex!(
    "93e02b6052719f607dacd3a088274f65596bd0d09920b61ab5da61bbdc7f5049334cf11213945d57e5ac7d055d042b7e\
     024aa2b2f08f0a91260805272dc51051c6e47ad4fa403b02b4510b647ae3d1770bac0326a805bbefd48056c8c121bdb8"
);

pub fn g() -> G1Projective {
    G1Affine::from_compressed(&G_BYTES).unwrap().into()
}

pub fn h() -> G1Projective {
    G1Affine::from_compressed(&H_BYTES).unwrap().into()
}

pub fn q() -> G2Projective {
    G2Affine::from_compressed(&Q_BYTES).unwrap().into()
}

// for testing
pub fn decompress(hex_str: &str) -> G1Projective {
    let bytes: Vec<u8> = hex::decode(hex_str).expect("invalid hex");
    let mut buf: [u8; 48] = [0u8; 48];
    buf.copy_from_slice(&bytes[..48]);
    let affine: G1Affine = G1Affine::from_compressed(&buf).unwrap();
    affine.into()
}

pub fn sk_to_g1(generator: &str, sk: Scalar) -> String {
    let point = decompress(generator) * sk;
    let compressed = point.to_affine().to_compressed();
    hex::encode(compressed)
}