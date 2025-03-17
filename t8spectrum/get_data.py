import numpy as np
import requests

from t8spectrum.url_params import UrlParams
from t8spectrum.util.decoder import zint_to_float


def get_waveform(url_params: UrlParams) -> tuple[np.ndarray, int]:
    """
    Fetches waveform data from a specified host.

    Args:
        url_params (UrlParams): The URL parameters

    Returns:
        tuple[np.ndarray, int]: A tuple containing the waveform data as a numpy array
            and the sample rate as an integer.

    Raises:
        Exception: If the request to fetch the waveform data fails.
    """
    url = url_params.generate_url("waves")
    response = requests.get(url, auth=(url_params.t8_user, url_params.t8_password))
    if response.status_code != 200:
        raise Exception(f"Failed to get waveform: {response.text}")
    response = response.json()

    waveform = zint_to_float(response["data"])
    factor = response["factor"]
    sample_rate = response["sample_rate"]

    return waveform * factor, sample_rate


def get_spectra(url_params: UrlParams) -> tuple[np.ndarray]:
    """
    Fetches spectral data from a specified host and endpoint.

    Args:
        url_params (UrlParams): The URL parameters object.

    Returns:
        tuple[np.ndarray]: A tuple containing the spectral data as numpy arrays.

    Raises:
        Exception: If the request to the server fails.
    """
    url = url_params.generate_url("spectra")
    response = requests.get(url, auth=(url_params.t8_user, url_params.t8_password))
    if response.status_code != 200:
        raise Exception(f"Failed to get spectra: {response.text}")
    response = response.json()

    spectrum = zint_to_float(response["data"])
    factor = response["factor"]
    fmin = response.get("min_freq", 0)
    fmax = response["max_freq"]

    return spectrum * factor, fmin, fmax
