from datetime import UTC, datetime


def datetime_to_timestamp(time: datetime | int) -> int:
    """
    Converts a datetime object to a timestamp. If it is already an integer, it is
    returned as is.

    Args:
        time (datetime | int): A datetime object or an integer representing a timestamp.

    Returns:
        int: The corresponding timestamp as an integer.
    """
    return int(time.timestamp()) if type(time) is datetime else time


def timestamp_to_iso_string(timestamp: int) -> str:
    """
    Convert a Unix timestamp to an ISO 8601 formatted string.

    Args:
        timestamp (int): The Unix timestamp to convert.

    Returns:
        str: The ISO 8601 formatted string representation of the timestamp.
    """
    return datetime.fromtimestamp(timestamp, tz=UTC).strftime("%Y-%m-%dT%H:%M:%S")


def iso_string_to_timestamp(iso_string: str) -> int:
    """
    Convert an ISO 8601 formatted string to a Unix timestamp.

    Args:
        iso_string (str): The ISO 8601 formatted string to convert.

    Returns:
        int: The Unix timestamp representation of the ISO 8601 formatted string.
    """
    return int(datetime.fromisoformat(iso_string).replace(tzinfo=UTC).timestamp())
