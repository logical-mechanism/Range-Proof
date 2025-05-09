// use aiken/cbor.{serialise}
use aiken/crypto/bls12_381/g1
use aiken/crypto/bls12_381/scalar.{Scalar}
use constants.{g, h}
use pedersen.{commitment}
use range.{RangeProof}
use schnorr.{SchnorrProof, fiat_shamir_heuristic}

pub type ZKInterval {
  // the range proof
  rp: RangeProof,
  // the schnorr proof for upper bound a
  spa: SchnorrProof,
  // the schnorr proof for lower bound b
  spb: SchnorrProof,
  // the upper bound a
  a: Int,
  // the lower bound b
  b: Int,
}

pub fn prove(zki: ZKInterval) -> Bool {
  //
  // turn the bounds into scalars
  expect Some(a): Option<Scalar> = scalar.new(zki.a)
  expect Some(b): Option<Scalar> = scalar.new(zki.b)
  //
  // the randomness of the upper bound commitment
  let ar: ByteArray =
    g1.sub(g1.decompress(zki.rp.ab), g1.scale(h, a)) |> g1.compress
  //
  // the randomness of the lower bound commitment
  let br: ByteArray =
    g1.sub(g1.decompress(zki.rp.bb), g1.scale(h, b)) |> g1.compress
  //
  // zk interval is the range proof plus schnorr proofs for the bounds
  and {
    range.prove(zki.rp)?,
    schnorr.prove(zki.spa, ar)?,
    schnorr.prove(zki.spb, br)?,
  }
}

test build_a_zk_interval_proof() {
  // max value
  let a: Int = 10
  // min value
  let b: Int = 0
  // that value to prove in the range
  let d: Int = 7
  // compute the range proof
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
  // trace rp
  // prove a
  expect Some(x): Option<Scalar> = scalar.new(1)
  expect Some(r): Option<Scalar> = scalar.new(321)
  let avalue: G1Element = g1.scale(g, x)
  let ag_r_b: ByteArray = g1.scale(g, r) |> g1.compress
  expect Some(c): Option<Scalar> =
    fiat_shamir_heuristic(g |> g1.compress, ag_r_b, avalue |> g1.compress)
      |> scalar.from_bytearray_big_endian()
  let z: Scalar = scalar.add(r, scalar.mul(x, c))
  let spa: SchnorrProof =
    SchnorrProof { z_b: scalar.to_bytearray_big_endian(z, 0), g_r_b: ag_r_b }
  // trace spa
  // prove b
  let bvalue: G1Element = g1.scale(g, x)
  let bg_r_b: ByteArray = g1.scale(g, r) |> g1.compress
  expect Some(c): Option<Scalar> =
    fiat_shamir_heuristic(g |> g1.compress, bg_r_b, bvalue |> g1.compress)
      |> scalar.from_bytearray_big_endian()
  let z: Scalar = scalar.add(r, scalar.mul(x, c))
  let spb: SchnorrProof =
    SchnorrProof { z_b: scalar.to_bytearray_big_endian(z, 0), g_r_b: bg_r_b }
  // trace spb
  // build the zk interval proof
  let zki: ZKInterval = ZKInterval { rp, spa, spb, a, b }
  prove(zki)
}

test a_zk_interval_proof() {
  let zki: ZKInterval =
    ZKInterval {
      rp: RangeProof {
        yb: #"b928f3beb93519eecf0145da903b40a4c97dca00b21f12ac0df3be9116ef2ef27b2ae6bcd4c5bc2d54ef5a70627efcb7",
        db: #"ad84464b3966ec5bede84aa487facfca7823af383715078da03b387cc2f5d5597cdd7d025aa07db00a38b953bdeb6e3f",
        pb: #"89ece308f9d1f0131765212deca99697b112d61f9be9a5f1f3780a51335b3ff981747a0b2ca2179b96d2c0c9024e5224",
        ab: #"9780e853f8ce7eda772c6691d25e220ca1d2ab0db51a7824b700620f7ac94c06639e91c98bb6abd78128f0ec845df8ef",
        bb: #"97f1d3a73197d7942695638c4fa9ac0fc3688c4f9774b905a14e3a3f171bac586c55e83ff97a1aeffb3af00adb22c6bb",
        wb: #"8d9e19b3f4c7c233a6112e5397309f9812a4f61f754f11dd3dcb8b07d55a7b1dfea65f19a1488a14fef9a41495083582",
        lb: #"89ece308f9d1f0131765212deca99697b112d61f9be9a5f1f3780a51335b3ff981747a0b2ca2179b96d2c0c9024e5224",
      },
      spa: SchnorrProof {
        z_b: #"45e8b989d0f75db379c4fe6c44e985405658805fb2133ad9fe92c682",
        g_r_b: #"8f5dd46d79e059c0a234b0e91f16b46aabf97ce030e99f997a2ab8da5b283474485d167e1060aabecb5e3c44aaba44a2",
      },
      spb: SchnorrProof {
        z_b: #"45e8b989d0f75db379c4fe6c44e985405658805fb2133ad9fe92c682",
        g_r_b: #"8f5dd46d79e059c0a234b0e91f16b46aabf97ce030e99f997a2ab8da5b283474485d167e1060aabecb5e3c44aaba44a2",
      },
      a: 10,
      b: 0,
    }
  prove(zki)
}

test a_bad_zk_interval_proof() fail {
  let zki: ZKInterval =
    ZKInterval {
      rp: RangeProof {
        yb: #"b928f3beb93519eecf0145da903b40a4c97dca00b21f12ac0df3be9116ef2ef27b2ae6bcd4c5bc2d54ef5a70627efcb7",
        db: #"ad84464b3966ec5bede84aa487facfca7823af383715078da03b387cc2f5d5597cdd7d025aa07db00a38b953bdeb6e3f",
        pb: #"89ece308f9d1f0131765212deca99697b112d61f9be9a5f1f3780a51335b3ff981747a0b2ca2179b96d2c0c9024e5224",
        ab: #"9780e853f8ce7eda772c6691d25e220ca1d2ab0db51a7824b700620f7ac94c06639e91c98bb6abd78128f0ec845df8ef",
        bb: #"97f1d3a73197d7942695638c4fa9ac0fc3688c4f9774b905a14e3a3f171bac586c55e83ff97a1aeffb3af00adb22c6bb",
        wb: #"8d9e19b3f4c7c233a6112e5397309f9812a4f61f754f11dd3dcb8b07d55a7b1dfea65f19a1488a14fef9a41495083582",
        lb: #"89ece308f9d1f0131765212deca99697b112d61f9be9a5f1f3780a51335b3ff981747a0b2ca2179b96d2c0c9024e5224",
      },
      spa: SchnorrProof {
        z_b: #"45e8b989d0f75db379c4fe6c44e985405658805fb2133ad9fe92c682",
        g_r_b: #"8f5dd46d79e059c0a234b0e91f16b46aabf97ce030e99f997a2ab8da5b283474485d167e1060aabecb5e3c44aaba44a2",
      },
      spb: SchnorrProof {
        z_b: #"45e8b989d0f75db379c4fe6c44e985405658805fb2133ad9fe92c682",
        g_r_b: #"8f5dd46d79e059c0a234b0e91f16b46aabf97ce030e99f997a2ab8da5b283474485d167e1060aabecb5e3c44aaba44a2",
      },
      // this is not the real upper bound
      a: 100000,
      b: 0,
    }
  prove(zki)
}

test real_zk_interval_proof1() {
  let zki: ZKInterval =
    ZKInterval {
      rp: RangeProof {
        yb: #"80a8871fdc79aee14b24be6493344c74d71a6e33a18903ed55e032ae510aa0587919b101005783809fdaea0b6dbbe223",
        db: #"8ffb4315e16fa8bc295e27187a706c8431adacbbcfd5dbb1b0719b4e995031006f28ac67259d4a042a027e9f26cc7316",
        pb: #"950b1b8c1f76a834dff18fdfb7699a05b5927d4663d7e90be6fd88488ee28a83ae401a06d2743c88a7ea92cafef31180",
        ab: #"90aade2b7b38e7d99b549d520e81251501397232104dba6384a5633242e5ca882e31088d563185c0ae0ae699be38ce08",
        bb: #"81fa8b6f0861dc60a0edd8e9542472ca07ff1f122b6ef30344d3448c74d9202a2e331b83910ac624874dc14a6a88abef",
        wb: #"ad034e8f2ff079510932486e05129fb3c04e68a17f44f86115403cebb9917001314e63a1c608c605ec2011ddd73ee4fc",
        lb: #"8d492cace882a1d8e92b6a4f4c9f2f629d0d830f5e42fa9d7502c556c0593249bf27630d96d6ae67feb50cb98c16a374",
      },
      spa: SchnorrProof {
        z_b: #"02a9843cb426bbfd93b9b7280b2dbd49385970d535f3084ed4280ccbb06070e4",
        g_r_b: #"aae176bf3c9480aa106a359d8b6b90c2e3967128b9c6dee5c4ed61132af0aaa126ce210cd6875818b29d6534f789c84a",
      },
      spb: SchnorrProof {
        z_b: #"234c808f2848f21ada85a89f8c450b90f31ec14843c7a713685e5ac6c85a5c93",
        g_r_b: #"9172117683335c9d4b2f695abfb906df2eb315c42d55fd401ea984cc97bf5a8cfbb706f98bb43ccc23ba66b43d1949d9",
      },
      a: 50,
      b: 10,
    }
  prove(zki)
}

test real_zk_interval_proof2() {
  let zki: ZKInterval =
    ZKInterval {
      rp: RangeProof {
        yb: #"abfe23767dbeb62d76ee24c52467cb19b2e6355be9e2718f8737fac68a87380f27f8533357ec633a28353ec22a674cf8",
        db: #"98ec59154736f7876c182e59dc4c4a72c522b9c42dda76efc3890f9768c9b92a33de38d106a8a6bafff9ceeb6310ac32",
        pb: #"8b5a26346a6c55d55469b24535b7485936fac77e892b5058c1386b420bf1211db9a29f285bb882bccc1173c8f662ca5e",
        ab: #"9337c578adb0e080ab31139ffd1f5b4629a02b884cfc472c4ed78fe34b8720d1ebc6043b6e8030bdd31a61ca5c7b3891",
        bb: #"8bb21c2ffb1046f01e63b0c699863bb377053ccf5aca6644635ee54c214f741676a6926fae8fbdc859a2370211aaa3dd",
        wb: #"9746326664b6d0c259be6b38d2d58e0d806ef554ab9f2babb51ecff91efae63cee22ab28acf7d3ecc8a8c246d0df38f8",
        lb: #"b96f36cf0acaf85c021e6823511839633deaf1cea6898631289943f53cf6cdcd97806651d33b192634d90c6982389409",
      },
      spa: SchnorrProof {
        z_b: #"09035341e6535331c3dea3db33a3c5d28b592c9c232574f333399e41147c0267",
        g_r_b: #"9119e038df86936a0b3adc24eed7def148c4d9c08a7c4c84006f7f69d94dfeae623241a86add0960059c9c6dc763a011",
      },
      spb: SchnorrProof {
        z_b: #"70c6b4eccaab139bc2a336ff81695c42567f699468b33e72e19aa52f729f6162",
        g_r_b: #"ae620e5065a9eea1e68e5703954b623e14cbbab43e85d9b676a3a25f104ec9c6f857fa414f87857775fe3c1003e725b7",
      },
      a: 100,
      b: 0,
    }
  prove(zki)
}

test range_proof_64_bit() {
  let zki: ZKInterval =
    ZKInterval {
      rp: RangeProof {
        yb: #"91e788a8d637867e6d5aa08f681951e0747c8d366e94516cfbea2eac9d6a5599abedb0cb5635c734e8e73fb441ddec22",
        db: #"ac0df002362bbce742e3c5f0dc4089836f4bcf330d958e3e8eb03d9a0007deaf40848f04caeaad9980bd109751b39ad8",
        pb: #"96656e6c6b2c6588f90e785501d05fcf2887fa47d0651cb4be9a21e5e5c2a9d3ca0c74172a1819255727ff35e9a74b06",
        ab: #"86ec2652196645493b5dcfc8b39395da79f7772cd10679febe93e4647c7ca15c3c04dde89801a30dae55f2212f1eb00c",
        bb: #"ab530039af16ea0d8429aa3de557a840f86918e1c9398a2b33e8bc35d64cdac246d59fa4edd1865c0fb10cbd43f79e27",
        wb: #"a3803f915947c40e28552e208135a00ff944784232004576e3a62799bb032e601f9d50d4815e826d22223f83d0d2bf17",
        lb: #"ad7c70488cb25379aaa55bb198ab4db882ecd7653a494d3018e53514fcfded06435b30257b859cc7025e90771f8e4c5d",
      },
      spa: SchnorrProof {
        z_b: #"059d2dd4747cd362b920c6ede86f6fa85bf7f9c1332553029711aa009363deea",
        g_r_b: #"b68e696a3aad260b451b3c9065d6433a91db539408303da23728dafb1af6ebf41c3ffacff53006dcb260e245e99bf9d6",
      },
      spb: SchnorrProof {
        z_b: #"2f0a8a5ebe71a9b06542e5e11dfdd27cd18b394b097941ef6298f7c5a2765dee",
        g_r_b: #"8e062b0795a0e4e7c071565016e084f1495db3e6bdbaec5867446e5847fe58d8243b059c8e8a8aa0ff5611b126614252",
      },
      a: 18446744073709551616,
      b: 0,
    }
  // trace serialise(zki)
  prove(zki)
}
