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
    t8_password: str,
) -> tuple[np.ndarray, int]:
    """
    Fetches waveform data from a specified host.

    Args:
        host (str): The hostname or IP address of the server.
        id (str): The T8 ID.
        machine (str): The machine identifier.
        point (str): The point tag.
        pmode (str): The processing mode tag.
        time (datetime | int): The waveform timestamp, either as a datetime object or an
            integer timestamp.
        t8_user (str): The username for authentication.
        t8_password (str): The password for authentication.

    Returns:
        tuple[np.ndarray, int]: A tuple containing the waveform data as a numpy array
            and the sample rate as an integer.

    Raises:
        Exception: If the request to fetch the waveform data fails.
    """
    if type(time) is datetime:
        time = int(time.timestamp())

    url = f"https://{host}/{id}/rest/waves/{machine}/{point}/{pmode}/{time}"
    response = requests.get(url, auth=(t8_user, t8_password))
    if response.status_code != 200:
        raise Exception(f"Failed to get waveform: {response.text}")

    waveform = zint_to_float(response.json()["data"])
    sample_rate = response.json()["sample_rate"]

    return waveform, sample_rate


def get_spectra(
    host: str,
    id: str,
    machine: str,
    point: str,
    pmode: str,
    time: datetime | int,
    t8_user: str,
    t8_password: str,
) -> tuple[np.ndarray]:
    """
    Fetches spectral data from a specified host and endpoint.

    Args:
        host (str): The hostname of the server.
        id (str): The identifier for the spectra.
        machine (str): The machine identifier.
        point (str): The point identifier.
        pmode (str): The mode of the spectra.
        time (datetime | int): The time of the spectra, either as a datetime object or a
            Unix timestamp.
        t8_user (str): The username for authentication.
        t8_password (str): The password for authentication.

    Returns:
        tuple[np.ndarray]: A tuple containing the spectral data as numpy arrays.

    Raises:
        Exception: If the request to the server fails.
    """
    if type(time) is datetime:
        time = int(time.timestamp())

    url = f"https://{host}/{id}/rest/spectra/{machine}/{point}/{pmode}/{time}"
    response = requests.get(url, auth=(t8_user, t8_password))
    if response.status_code != 200:
        raise Exception(f"Failed to get spectra: {response.text}")

    spectrum = zint_to_float(response.json()["data"])
    factor = response.json()["factor"]

    return spectrum * factor
