from unittest.mock import patch

import numpy as np
import pytest

from t8_client import get_data


def test_get_wave_list_success() -> None:
    """
    Test the successful retrieval of wave list.

    This test mocks the response from the `requests.get` call to simulate
    retrieving a list of wave links. It then verifies that the `get_wave_list`
    function correctly processes the response and returns the expected list
    of timestamps.

    The mock response contains three wave links with specific timestamps.
    The test checks that the `get_wave_list` function extracts these timestamps
    correctly and returns them in the expected format.

    Mocks:
        requests.get: Mocked to return a predefined response with wave links.

    Asserts:
        The result of `get_wave_list` matches the expected list of timestamps.
    """
    mock_response = {
        "_items": [
            {
                "_links": {
                    "self": "http://lzfs45.mirror.twave.io/lzfs45/rest/waves/LP_Turbine/MAD31CY005/AM1/1554907724"
                }
            },
            {
                "_links": {
                    "self": "http://lzfs45.mirror.twave.io/lzfs45/rest/waves/LP_Turbine/MAD31CY005/AM1/1554907764"
                }
            },
            {
                "_links": {
                    "self": "http://lzfs45.mirror.twave.io/lzfs45/rest/waves/LP_Turbine/MAD31CY005/AM1/1554907768"
                }
            },
        ],
    }

    kwargs = {
        "host": "example.com",
        "id": "test_id",
        "machine": "test_machine",
        "point": "test_point",
        "pmode": "test_pmode",
        "t8_user": "user",
        "t8_password": "password",
    }

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = list(get_data.get_wave_list(**kwargs))
        assert result == [
            "2019-04-10T14:48:44",
            "2019-04-10T14:49:24",
            "2019-04-10T14:49:28",
        ]


def test_get_wave_list_failure() -> None:
    """
    Test case for get_wave_list function when the request fails.

    This test simulates a failure scenario where the HTTP GET request to fetch the wave
    list returns a 404 status code with a "Not Found" message. It verifies that the
    function raises an exception with the appropriate error message.

    Steps:
    1. Define the necessary keyword arguments for the get_wave_list function.
    2. Mock the 'requests.get' method to return a 404 status code and "Not Found" text.
    3. Call the get_wave_list function with the mocked response and check if it raises
       an exception.
    4. Assert that the exception message contains "Failed to get waveform: Not Found".

    Expected Result:
    The test should pass if the get_wave_list function raises an exception with the
    message "Failed to get waveform: Not Found" when the HTTP GET request fails with a
    404 status code.
    """
    kwargs = {
        "host": "example.com",
        "id": "test_id",
        "machine": "M1",
        "point": "P1",
        "pmode": "PM1",
        "t8_user": "user",
        "t8_password": "password",
    }

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = "Not Found"

        with pytest.raises(Exception) as excinfo:
            list(get_data.get_wave_list(**kwargs))
        assert "Failed to get waveform: Not Found" in str(excinfo.value)


def test_get_wave_success() -> None:
    """
    Test the `get_wave` function from the `get_data` module for successful data
    retrieval.

    This test mocks the `requests.get` method to simulate an API response and verifies
    that the `get_wave` function correctly processes the response data.

    The mock response contains:
    - Base64 encoded data
    - A factor to multiply the decoded data
    - A sample rate

    The test verifies that:
    - The decoded and scaled data matches the expected numpy array.
    - The sample rate matches the expected value.

    Mocks:
    - `requests.get`: Simulates an API call and returns a predefined response.

    Assertions:
    - The decoded and scaled data is correctly processed.
    - The sample rate is correctly returned.
    """
    expected_sample_rate = 2560

    mock_response = {
        "data": "eJxjZPj//389QwMAEP4D/g==",
        "factor": 2.0,
        "sample_rate": expected_sample_rate,
    }

    kwargs = {
        "host": "example.com",
        "id": "test_id",
        "machine": "test_machine",
        "point": "test_point",
        "pmode": "test_pmode",
        "time": "2019-04-10T14:48:44",
        "t8_user": "user",
        "t8_password": "password",
    }

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_data.get_wave(**kwargs)
        assert np.array_equal(
            result[0], 2 * np.array([1.0000e00, -1.0000e00, 3.2767e04, -3.2768e04])
        )
        assert result[1] == expected_sample_rate


def test_get_wave_failure() -> None:
    """
    Test case for the `get_wave` function to handle failure scenarios.

    This test verifies that the `get_wave` function raises an exception when the
    HTTP request to retrieve waveform data fails with a 404 status code.

    Test Steps:
    1. Define the necessary keyword arguments for the `get_wave` function.
    2. Mock the `requests.get` method to simulate a 404 Not Found response.
    3. Call the `get_wave` function with the defined keyword arguments and expect
        it to raise an exception.
    4. Assert that the raised exception contains the expected error message.

    Expected Result:
    The test should pass if the `get_wave` function raises an exception with the
    message "Failed to get waveform: Not Found" when the HTTP request fails with
    a 404 status code.
    """
    kwargs = {
        "host": "example.com",
        "id": "test_id",
        "machine": "M1",
        "point": "P1",
        "pmode": "PM1",
        "time": "2019-04-10T14:48:44",
        "t8_user": "user",
        "t8_password": "password",
    }

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = "Not Found"

        with pytest.raises(Exception) as excinfo:
            get_data.get_wave(**kwargs)
        assert "Failed to get waveform: Not Found" in str(excinfo.value)


def test_get_spectra_success() -> None:
    """
    Test the successful retrieval of spectra data.

    This test mocks the response from an API call to retrieve spectra data and verifies
    that the `get_spectra` function processes the response correctly.

    The mock response contains three spectra items with their respective URLs. The test
    checks if the `get_spectra` function returns the correct timestamps extracted from
    the URLs.

    Mocks:
        - `requests.get`: Mocked to return a predefined response with a status code of
          200 and a JSON body containing spectra data.

    Assertions:
        - The result of `get_spectra` should be a list of timestamps corresponding to
          the spectra items in the mock response.
    """
    mock_response = {
        "_items": [
            {
                "_links": {
                    "self": "http://lzfs45.mirror.twave.io/lzfs45/rest/spectra/LP_Turbine/MAD31CY005/AM1/1554907724"
                }
            },
            {
                "_links": {
                    "self": "http://lzfs45.mirror.twave.io/lzfs45/rest/spectra/LP_Turbine/MAD31CY005/AM1/1554907764"
                }
            },
            {
                "_links": {
                    "self": "http://lzfs45.mirror.twave.io/lzfs45/rest/spectra/LP_Turbine/MAD31CY005/AM1/1554907768"
                }
            },
        ],
    }

    kwargs = {
        "host": "example.com",
        "id": "test_id",
        "machine": "test_machine",
        "point": "test_point",
        "pmode": "test_pmode",
        "t8_user": "user",
        "t8_password": "password",
    }

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = list(get_data.get_spectra(**kwargs))
        assert result == [
            "2019-04-10T14:48:44",
            "2019-04-10T14:49:24",
            "2019-04-10T14:49:28",
        ]


def test_get_spectra_failure() -> None:
    """
    Test case for the `get_spectra` function to handle failure scenarios.

    This test simulates a failure response from the `requests.get` call by mocking it to
    return a 404 status code with a "Not Found" message. It then verifies that the
    `get_spectra` function raises an exception with the appropriate error message.

    Tested function:
    - get_data.get_spectra

    Test steps:
    1. Define the necessary keyword arguments for the `get_spectra` function.
    2. Mock the `requests.get` method to return a 404 status code and "Not Found" text.
    3. Call the `get_spectra` function and expect it to raise an exception.
    4. Assert that the exception message contains "Failed to get spectra list: Not
       Found".

    Expected outcome:
    - The `get_spectra` function should raise an exception with the message "Failed to
      get spectra list: Not Found" when the `requests.get` call returns a 404 status
      code.
    """
    kwargs = {
        "host": "example.com",
        "id": "test_id",
        "machine": "M1",
        "point": "P1",
        "pmode": "PM1",
        "t8_user": "user",
        "t8_password": "password",
    }

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = "Not Found"

        with pytest.raises(Exception) as excinfo:
            list(get_data.get_spectra(**kwargs))
        assert "Failed to get spectra list: Not Found" in str(excinfo.value)


def test_get_spectrum_success() -> None:
    """
    Test the `get_spectrum` function for successful data retrieval.

    This test mocks the `requests.get` method to simulate a successful API response
    with predefined spectrum data. It verifies that the `get_spectrum` function
    correctly processes the response and returns the expected results.

    Mock Response:
        - data: Base64 encoded string representing the spectrum data.
        - factor: Scaling factor for the spectrum data.
        - min_freq: Minimum frequency of the spectrum.
        - max_freq: Maximum frequency of the spectrum.

    Test Parameters:
        - host: The host of the API.
        - id: The ID of the spectrum data.
        - machine: The machine identifier.
        - point: The point identifier.
        - pmode: The mode of the point.
        - time: The timestamp of the data.
        - t8_user: The username for authentication.
        - t8_password: The password for authentication.

    Assertions:
        - The returned spectrum data is correctly scaled and matches the expected array.
        - The minimum frequency matches the expected value.
        - The maximum frequency matches the expected value.
    """
    expected_fmin = 5
    expected_fmax = 20

    mock_response = {
        "data": "eJxjZPj//389QwMAEP4D/g==",
        "factor": 2.0,
        "min_freq": expected_fmin,
        "max_freq": expected_fmax,
    }

    kwargs = {
        "host": "example.com",
        "id": "test_id",
        "machine": "test_machine",
        "point": "test_point",
        "pmode": "test_pmode",
        "time": "2019-04-10T14:48:44",
        "t8_user": "user",
        "t8_password": "password",
    }

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        result = get_data.get_spectrum(**kwargs)
        assert np.array_equal(
            result[0], 2 * np.array([1.0000e00, -1.0000e00, 3.2767e04, -3.2768e04])
        )
        assert result[1] == expected_fmin
        assert result[2] == expected_fmax


def test_get_spectrum_failure() -> None:
    """
    Test case for the `get_spectrum` function to handle failure scenarios.

    This test verifies that the `get_spectrum` function raises an exception
    when the HTTP request to retrieve spectrum data fails with a 404 status code.

    Test Steps:
    1. Define the necessary keyword arguments for the `get_spectrum` function.
    2. Mock the `requests.get` method to simulate a 404 Not Found response.
    3. Call the `get_spectrum` function with the defined keyword arguments.
    4. Assert that an exception is raised with the expected error message.

    Expected Result:
    An exception is raised with the message "Failed to get spectra: Not Found".
    """
    kwargs = {
        "host": "example.com",
        "id": "test_id",
        "machine": "M1",
        "point": "P1",
        "pmode": "PM1",
        "time": "2019-04-10T14:48:44",
        "t8_user": "user",
        "t8_password": "password",
    }

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = "Not Found"

        with pytest.raises(Exception) as excinfo:
            get_data.get_spectrum(**kwargs)
        assert "Failed to get spectra: Not Found" in str(excinfo.value)
