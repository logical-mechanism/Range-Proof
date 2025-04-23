from src.blake2b_224 import fiat_shamir_heuristic, generate


def test_empty_string_hash():
    h = generate("")
    assert h == "836cc68931c2e4e3e838602eca1902591d216837bafddfe6f0c8cb07"


def test_hello_world_hash():
    input_string = "Hello, world!"
    h = generate(input_string)
    assert h == "e552ae1ccaacf44a0e1939b2f85fe39b9eb9f5fa6abb41560716dec1"


def test_empty_fiat_shamir_heuristic():
    fsh = fiat_shamir_heuristic("", "", "")
    assert fsh == "836cc68931c2e4e3e838602eca1902591d216837bafddfe6f0c8cb07"


def test_real_fiat_shamir_heuristic():
    fsh = fiat_shamir_heuristic(
        "86f0c64bd433568dd92751f0bee97feaaeee6f3c2144b210be68d2bc85253b1994703caf7f8361ccf246fef52c0ad859",
        "97f1d3a73197d7942695638c4fa9ac0fc3688c4f9774b905a14e3a3f171bac586c55e83ff97a1aeffb3af00adb22c6bb",
        "a2cbc5c3c72a7bc9047971345df392a67279d2f32082891976d913c699885c3ff9a90a8ea942bef4729cf93f526521e4",
    )
    assert fsh == "c4f2937e8317aee04a17b6ea65b2e3706aabd75dd2ebce5e6c8744ed"
