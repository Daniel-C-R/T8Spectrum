from datetime import datetime


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
