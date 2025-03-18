from t8_client.util.timestamp import timestamp_to_iso_string


def test_timestamp_to_iso_string():
    """
    Test the `timestamp_to_iso_string` function.

    This test checks if the `timestamp_to_iso_string` function correctly converts
    a given Unix timestamp to an ISO 8601 formatted string.

    Assertions:
        - The function should return the expected ISO 8601 string for the given
          timestamp.

    Tested values:
        - time: "2019-04-11T18:25:54"
        - timestamp: 1555007154
    """
    time = "2019-04-11T18:25:54"
    timestamp = 1555007154
    assert timestamp_to_iso_string(timestamp) == time
