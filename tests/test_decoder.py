from base64 import b64encode
from zlib import compress

import numpy as np
import pytest

from t8spectrum.util.decoder import zint_to_float


def test_zint_to_float():
    """
    Test the `zint_to_float` function.
    This test performs the following steps:
    1. Creates a sample array of 16-bit integers.
    2. Converts the sample data to bytes.
    3. Compresses the bytes.
    4. Encodes the compressed data to base64.
    5. Calls the `zint_to_float` function with the encoded data.
    6. Asserts that the result is as expected by comparing it to the sample data
       converted to 32-bit floats.
    The expected result is an array of the sample data converted to 32-bit floats.
    """
    # Create a sample array of 16-bit integers
    sample_data = np.array([1, -1, 32767, -32768], dtype=np.int16)

    # Convert the sample data to bytes
    sample_bytes = sample_data.tobytes()

    # Compress the bytes
    compressed_data = compress(sample_bytes)

    # Encode the compressed data to base64
    encoded_data = b64encode(compressed_data).decode()

    # Call the function to test
    result = zint_to_float(encoded_data)

    # Assert the result is as expected
    expected_result = sample_data.astype(np.float32)
    np.testing.assert_array_equal(result, expected_result)


def test_zint_to_float_empty_string():
    """
    Test the `zint_to_float` function with an empty string input.

    This test verifies that the `zint_to_float` function correctly handles an empty
    string by returning an empty NumPy array of type float32.

    Assertions:
        - The result should be an empty NumPy array of type float32.
    """
    # Test with an empty string
    result = zint_to_float("")
    expected_result = np.array([], dtype=np.float32)
    np.testing.assert_array_equal(result, expected_result)


def test_zint_to_float_invalid_data():
    """
    Test the zint_to_float function with invalid data.

    This test ensures that the zint_to_float function raises an exception
    when provided with an invalid base64 string. The function is expected
    to handle such cases gracefully by raising an appropriate exception.
    """
    # Test with invalid data
    with pytest.raises(ValueError):
        zint_to_float("invalid_base64")
