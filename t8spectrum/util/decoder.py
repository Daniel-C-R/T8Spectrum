from zlib import decompress
from base64 import b64decode
from struct import unpack

import numpy as np


def zint_to_float(raw):
    decompressed_data = decompress(b64decode(raw.encode()))
    return np.array([unpack('h', decompressed_data[i*2:(i+1)*2])[0] for i in range(int(len(decompressed_data)/2))], dtype='f')
