import numpy as np
import requests
from util.decoder import zint_to_float
from util.timestamp import datetime_to_timestamp


def get_waveform(**kwargs) -> tuple[np.ndarray, int]:
    """
    Fetches waveform data from a specified host.

    Args:
        kwargs: The URL parameters as keyword arguments.

    Returns:
        tuple[np.ndarray, int]: A tuple containing the waveform data as a numpy array
            and the sample rate as an integer.

    Raises:
        Exception: If the request to fetch the waveform data fails.
    """
    host = kwargs["host"]
    id_ = kwargs["id"]
    machine = kwargs["machine"]
    point = kwargs["point"]
    pmode = kwargs["pmode"]
    time = datetime_to_timestamp(kwargs["time"])
    t8_user = kwargs["t8_user"]
    t8_password = kwargs["t8_password"]

    url = f"https://{host}/{id_}/rest/waves/{machine}/{point}/{pmode}/{time}"
    response = requests.get(url, auth=(t8_user, t8_password))
    if response.status_code != 200:
        raise Exception(f"Failed to get waveform: {response.text}")
    response = response.json()

    waveform = zint_to_float(response["data"])
    factor = response["factor"]
    sample_rate = response["sample_rate"]

    return waveform * factor, sample_rate


def get_spectra(**kwargs) -> tuple[np.ndarray]:
    """
    Fetches spectral data from a specified host and endpoint.

    Args:
        kwargs: The URL parameters as keyword arguments.

    Returns:
        tuple[np.ndarray]: A tuple containing the spectral data as numpy arrays.

    Raises:
        Exception: If the request to the server fails.
    """
    host = kwargs["host"]
    id_ = kwargs["id"]
    machine = kwargs["machine"]
    point = kwargs["point"]
    pmode = kwargs["pmode"]
    time = datetime_to_timestamp(kwargs["time"])
    t8_user = kwargs["t8_user"]
    t8_password = kwargs["t8_password"]

    url = f"https://{host}/{id_}/rest/spectra/{machine}/{point}/{pmode}/{time}"
    response = requests.get(url, auth=(t8_user, t8_password))
    if response.status_code != 200:
        raise Exception(f"Failed to get spectra: {response.text}")
    response = response.json()

    spectrum = zint_to_float(response["data"])
    factor = response["factor"]
    fmin = response.get("min_freq", 0)
    fmax = response["max_freq"]

    return spectrum * factor, fmin, fmax
