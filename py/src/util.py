import binascii


def hexify(n: int) -> str:
    """
    Convert an integer to a hexadecimal string representation.

    Args:
        n (int): The integer to convert.

    Returns:
        str: The hexadecimal string representation of the integer.
    """
    hex_n = hex(n)[2:]  # Remove the '0x' prefix
    if len(hex_n) % 2 != 0:
        hex_n = "0" + hex_n  # Prepend '0' if length is odd
    return hex_n


def hex_encode(msg: str) -> str:
    """
    Encode a string into hexadecimal format.

    Args:
        msg (str): The input string to encode.

    Returns:
        str: The hexadecimal encoded string.
    """
    return binascii.hexlify(msg.encode()).decode()
