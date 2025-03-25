"""Module for fetching data from the T8 REST API."""

from collections.abc import Generator

import numpy as np
import requests

from t8_client import url_params
from t8_client.util.decoder import zint_to_float
from t8_client.util.timestamp import timestamp_to_iso_string


def get_wave_list(params: url_params.PmodeParams) -> Generator[str]:
    """Retrieve a list of wave timestamps from a specified host and endpoint.

    Args:
        params (url_params.PmodeParams): The URL parameters as a `PmodeParams` object

    Yields:
        str: ISO formatted timestamp string for each valid wave item.

    Raises:
        Exception: If the request to the server fails.

    """
    host = params.host
    id_ = params.id_
    machine = params.machine
    point = params.point
    pmode = params.pmode
    t8_user = params.user
    t8_password = params.password

    url = f"https://{host}/{id_}/rest/waves/{machine}/{point}/{pmode}"
    response = requests.get(url, auth=(t8_user, t8_password), timeout=10)
    if response.status_code != requests.codes.ALL_OK:
        error_message = f"Failed to get waveform: {response.text}"
        raise requests.HTTPError(error_message)
    response = response.json()

    for item in response["_items"]:
        timestamp = int(item["_links"]["self"].split("/")[-1])
        if timestamp != 0:
            yield timestamp_to_iso_string(timestamp)


def get_wave(params: url_params.PmodeTimeParams) -> tuple[np.ndarray, int]:
    """Fetch waveform data from a specified host.

    Args:
        params (url_params.PmodeTimeParams): The URL parameters as a `PmodeTimeParams`
            object.

    Returns:
        tuple[np.ndarray, int]: A tuple containing the waveform data as a numpy array
            and the sample rate as an integer.

    Raises:
        Exception: If the request to fetch the waveform data fails.

    """
    host = params.host
    id_ = params.id_
    machine = params.machine
    point = params.point
    pmode = params.pmode
    t8_user = params.user
    t8_password = params.password
    timestamp = params.time

    url = f"https://{host}/{id_}/rest/waves/{machine}/{point}/{pmode}/{timestamp}"
    response = requests.get(url, auth=(t8_user, t8_password), timeout=10)
    if response.status_code != requests.codes.ALL_OK:
        error_message = f"Failed to get waveform: {response.text}"
        raise requests.HTTPError(error_message)
    response = response.json()

    waveform = zint_to_float(response["data"])
    factor = response["factor"]
    sample_rate = response["sample_rate"]

    return waveform * factor, sample_rate


def get_spectra(params: url_params.PmodeParams) -> Generator[str]:
    """Fetch spectra data from a specified host and yields timestamps in ISO format.

    Args:
        params (url_params.PmodeParams): The URL parameters as a `PmodeParams` object.

    Yields:
        str: Timestamps in ISO format.

    Raises:
        Exception: If the request to get spectra list fails.

    """
    host = params.host
    id_ = params.id_
    machine = params.machine
    point = params.point
    pmode = params.pmode
    t8_user = params.user
    t8_password = params.password

    url = f"https://{host}/{id_}/rest/spectra/{machine}/{point}/{pmode}"
    response = requests.get(url, auth=(t8_user, t8_password), timeout=10)
    if response.status_code != requests.codes.ALL_OK:
        error_message = f"Failed to get spectra list: {response.text}"
        raise requests.HTTPError(error_message)
    response = response.json()

    for item in response["_items"]:
        timestamp = int(item["_links"]["self"].split("/")[-1])
        if timestamp != 0:
            yield timestamp_to_iso_string(timestamp)


def get_spectrum(params: url_params.PmodeTimeParams) -> tuple[np.ndarray]:
    """Fetch spectrum data from a specified host and endpoint.

    Args:
        params (url_params.PmodeTimeParams): The URL parameters as a `PmodeTimeParams`
            object.

    Returns:
        tuple[np.ndarray, int, int]: A tuple containing the spectral data as numpy
        arrays, the minimum frequency, and the maximum frequency.

    Raises:
        Exception: If the request to the server fails.

    """
    host = params.host
    id_ = params.id_
    machine = params.machine
    point = params.point
    pmode = params.pmode
    t8_user = params.user
    t8_password = params.password
    timestamp = params.time

    url = f"https://{host}/{id_}/rest/spectra/{machine}/{point}/{pmode}/{timestamp}"
    response = requests.get(url, auth=(t8_user, t8_password), timeout=10)
    if response.status_code != requests.codes.ALL_OK:
        error_message = f"Failed to get spectra: {response.text}"
        raise requests.HTTPError(error_message)
    response = response.json()

    spectrum = zint_to_float(response["data"])
    factor = response["factor"]
    fmin = response.get("min_freq", 0)
    fmax = response["max_freq"]

    return spectrum * factor, fmin, fmax
