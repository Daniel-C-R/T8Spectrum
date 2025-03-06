from datetime import datetime
import numpy as np

import requests


from t8spectrum.util.decoder import zint_to_float


def get_waveform(
        host: str,
        id: str,
        machine: str,
        point: str,
        pmode: str,
        time: datetime | int,
        t8_user: str,
        t8_password: str
) -> tuple[np.ndarray, int]:
    """
    Fetches waveform data from a specified host.

    Args:
        host (str): The hostname or IP address of the server.
        id (str): The T8 ID.
        machine (str): The machine identifier.
        point (str): The point tag.
        pmode (str): The processing mode tag.
        time (datetime | int): The waveform timestamp, either as a datetime object or an integer timestamp.
        t8_user (str): The username for authentication.
        t8_password (str): The password for authentication.

    Returns:
        tuple[np.ndarray, int]: A tuple containing the waveform data as a numpy array and the sample rate as an integer.

    Raises:
        Exception: If the request to fetch the waveform data fails.
    """
    if type(time) is datetime:
        time = time.timestamp()

    url = f"https://{host}/{id}/rest/waves/{machine}/{point}/{pmode}/{time}"
    response = requests.get(url, auth=(t8_user, t8_password))
    if response.status_code != 200:
        raise Exception(f"Failed to get waveform: {response.text}")

    waveform = zint_to_float(response.json()["data"])
    sample_rate = response.json()["sample_rate"]

    return waveform, sample_rate
