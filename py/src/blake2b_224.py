from binascii import unhexlify
from hashlib import blake2b


def hash_function() -> type[blake2b]:
    """
    Assigns sha3_256 as a hash function for the hash to g2 function inside the bls12-381 module.

    Returns:
        function: The sha3_256 function
    """
    return blake2b


def generate(input_string: str) -> str:
    """
    Calculates the SHA3-256 hash digest of the input string.

    Args:
        input_string (str): The string to be hashed.

    Returns:
        str: The SHA3-256 hash digest of the input string.
    """
    # Encode the input string to bytes before hashing
    encoded_string = input_string.encode('utf-8')

    # Calculate the hash digest using SHA3-256
    hash_digest = blake2b(encoded_string, digest_size=28).hexdigest()

    return hash_digest


def fiat_shamir_heuristic(gb: str, grb: str, ub: str) -> str:
    """
    Applies the Fiat-Shamir heuristic to generate a hash.

    Parameters:
    gb (str): The first input string, typically representing a value in hex.
    grb (str): The second input string, typically representing a value in hex.
    ub (str): The third input string, typically representing a value in hex.

    Returns:
    str: The resulting hash as a hexadecimal string.
    """
    # Concatenate the input strings
    concatenated_bytes = gb + grb + ub

    # Convert the concatenated hex string to bytes
    unhexed_bytes = unhexlify(concatenated_bytes)

    # Compute the SHA-3 (256-bit) hash of the bytes and convert to a hex string
    hash_result = blake2b(unhexed_bytes, digest_size=28).digest().hex()

    return hash_result
