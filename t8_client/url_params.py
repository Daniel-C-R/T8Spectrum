"""Data models for URL parameters."""

from typing import Annotated

from pydantic import BaseModel, BeforeValidator

from t8_client.util.timestamp import iso_string_to_timestamp


class CredentialParams(BaseModel):
    """Represents the parameters required for the host and authentication.

    CredentialParams is a data model that represents the parameters required for
    authentication.

    Attributes:
        host (str): The hostname or IP address of the server.
        id_ (str): The unique identifier for the credential.
        user (str): The username for authentication.
        password (str): The password for authentication.
    """

    host: str
    id_: str
    user: str
    password: str


class PmodeParams(CredentialParams):
    """Represents parameters related to a specific processing mode.

    PmodeParams is a data class that inherits from CredentialParams and is used to store
    parameters related to a specific operational mode.

    Attributes:
        machine (str): The identifier for the machine.
        point (str): The specific point or location associated with the parameters.
        pmode (str): The operational mode or configuration.

    """

    machine: str
    point: str
    pmode: str


class PmodeTimeParams(PmodeParams):
    """Represents parameters related to a specific processing mode and time.

    PmodeTimeParams is a subclass of PmodeParams that represents parameters
    related to time. It includes a single attribute:

    Attributes:
        time (int): A timestamp represented as an integer. The value is validated and
            converted from an ISO 8601 formatted string to a timestamp using the
            `iso_string_to_timestamp` function before being assigned.

    """

    time: Annotated[int, BeforeValidator(iso_string_to_timestamp)]
