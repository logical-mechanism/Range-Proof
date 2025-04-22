use aiken/builtin

// g^1
pub const g: G1Element =
  #<Bls12_381, G1>"97f1d3a73197d7942695638c4fa9ac0fc3688c4f9774b905a14e3a3f171bac586c55e83ff97a1aeffb3af00adb22c6bb"

// g^2
pub const h: G1Element =
  #<Bls12_381, G1>"a572cbea904d67468808c8eb50a9450c9721db309128012543902d0ac358a62ae28f75bb8f1c7c42c39a8c5529bf0f4e"

// q^1
pub const q: G2Element =
  #<Bls12_381, G2>"93e02b6052719f607dacd3a088274f65596bd0d09920b61ab5da61bbdc7f5049334cf11213945d57e5ac7d055d042b7e024aa2b2f08f0a91260805272dc51051c6e47ad4fa403b02b4510b647ae3d1770bac0326a805bbefd48056c8c121bdb8"

test create_g() {
  builtin.bls12_381_g1_scalar_mul(1, g) == g
}

test add_g_to_h() {
  builtin.bls12_381_g1_add(g, g) == h
}

test create_h() {
  builtin.bls12_381_g1_scalar_mul(2, g) == h
}

test create_q() {
  builtin.bls12_381_g2_scalar_mul(1, q) == q
}
