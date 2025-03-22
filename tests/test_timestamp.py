from t8_client.util.timestamp import iso_string_to_timestamp, timestamp_to_iso_string


def test_timestamp_to_iso_string() -> None:
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


def test_iso_string_to_timestamp() -> None:
    """
    Test the `iso_string_to_timestamp` function.

    This test checks if the `iso_string_to_timestamp` function correctly converts
    a given ISO 8601 formatted string to a Unix timestamp.

    Assertions:
        - The function should return the expected Unix timestamp for the given
            ISO 8601 string.

    Tested values:
        - iso_string: "2019-04-11T18:25:54"
        - timestamp: 1555007154
    """
    iso_string = "2019-04-11T18:25:54"
    timestamp = 1555007154
    assert iso_string_to_timestamp(iso_string) == timestamp
