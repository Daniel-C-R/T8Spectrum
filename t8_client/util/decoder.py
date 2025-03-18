from base64 import b64decode
from struct import unpack
from zlib import decompress

import numpy as np


def zint_to_float(raw):
    """
    Convert a base64 encoded compressed string of 16-bit integers to a NumPy array of
        floats.

    Args:
        raw (str): A base64 encoded string containing compressed 16-bit integer data.

    Returns:
        np.ndarray: A NumPy array of floats obtained by decompressing and decoding the
            input string.
    """
    if not raw:
        return np.array([], dtype="f")

    decompressed_data = decompress(b64decode(raw.encode()))
    return np.array(
        [
            unpack("h", decompressed_data[i * 2 : (i + 1) * 2])[0]
            for i in range(int(len(decompressed_data) / 2))
        ],
        dtype="f",
    )
