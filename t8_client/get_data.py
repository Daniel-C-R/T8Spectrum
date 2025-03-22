from collections.abc import Generator

import numpy as np
import requests

from t8_client.util.decoder import zint_to_float
from t8_client.util.timestamp import iso_string_to_timestamp, timestamp_to_iso_string

HTTP_STATUS_OK = 200


def get_wave_list(**kwargs: dict) -> Generator[str]:
    """
    Retrieves a list of wave timestamps from a specified host and endpoint.

    Args:
        **kwargs: Arbitrary keyword arguments.
            host (str): The host URL.
            id_ (str): The ID for the endpoint.
            machine (str): The machine identifier.
            point (str): The point identifier.
            pmode (str): The mode parameter.
            t8_user (str): The username for authentication.
            t8_password (str): The password for authentication.

    Yields:
        str: ISO formatted timestamp string for each valid wave item.

    Raises:
        Exception: If the request to the server fails.
    """
    host = kwargs["host"]
    id_ = kwargs["id"]
    machine = kwargs["machine"]
    point = kwargs["point"]
    pmode = kwargs["pmode"]
    t8_user = kwargs["t8_user"]
    t8_password = kwargs["t8_password"]

    url = f"https://{host}/{id_}/rest/waves/{machine}/{point}/{pmode}"
    response = requests.get(url, auth=(t8_user, t8_password))
    if response.status_code != HTTP_STATUS_OK:
        raise Exception(f"Failed to get waveform: {response.text}")
    response = response.json()

    for item in response["_items"]:
        timestamp = int(item["_links"]["self"].split("/")[-1])
        if timestamp != 0:
            yield timestamp_to_iso_string(timestamp)


def get_wave(**kwargs: dict) -> tuple[np.ndarray, int]:
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
    time = iso_string_to_timestamp(kwargs["time"])
    t8_user = kwargs["t8_user"]
    t8_password = kwargs["t8_password"]

    url = f"https://{host}/{id_}/rest/waves/{machine}/{point}/{pmode}/{time}"
    response = requests.get(url, auth=(t8_user, t8_password))
    if response.status_code != HTTP_STATUS_OK:
        raise Exception(f"Failed to get waveform: {response.text}")
    response = response.json()

    waveform = zint_to_float(response["data"])
    factor = response["factor"]
    sample_rate = response["sample_rate"]

    return waveform * factor, sample_rate


def get_spectra(**kwargs: dict) -> Generator[str]:
    """
    Fetches spectra data from a specified host and yields timestamps in ISO format.

    Args:
        host (str): The host URL.
        id_ (str): The ID for the spectra request.
        machine (str): The machine identifier.
        point (str): The point identifier.
        pmode (str): The mode of the spectra.
        t8_user (str): The username for authentication.
        t8_password (str): The password for authentication.

    Yields:
        str: Timestamps in ISO format.

    Raises:
        Exception: If the request to get spectra list fails.
    """
    host = kwargs["host"]
    id_ = kwargs["id"]
    machine = kwargs["machine"]
    point = kwargs["point"]
    pmode = kwargs["pmode"]
    t8_user = kwargs["t8_user"]
    t8_password = kwargs["t8_password"]

    url = f"https://{host}/{id_}/rest/spectra/{machine}/{point}/{pmode}"
    response = requests.get(url, auth=(t8_user, t8_password))
    if response.status_code != HTTP_STATUS_OK:
        raise Exception(f"Failed to get spectra list: {response.text}")
    response = response.json()

    for item in response["_items"]:
        timestamp = int(item["_links"]["self"].split("/")[-1])
        if timestamp != 0:
            yield timestamp_to_iso_string(timestamp)


def get_spectrum(**kwargs: dict) -> tuple[np.ndarray]:
    """
    Fetches spectrum data from a specified host and endpoint.

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
    time = iso_string_to_timestamp(kwargs["time"])
    t8_user = kwargs["t8_user"]
    t8_password = kwargs["t8_password"]

    url = f"https://{host}/{id_}/rest/spectra/{machine}/{point}/{pmode}/{time}"
    response = requests.get(url, auth=(t8_user, t8_password))
    if response.status_code != HTTP_STATUS_OK:
        raise Exception(f"Failed to get spectra: {response.text}")
    response = response.json()

    spectrum = zint_to_float(response["data"])
    factor = response["factor"]
    fmin = response.get("min_freq", 0)
    fmax = response["max_freq"]

    return spectrum * factor, fmin, fmax
