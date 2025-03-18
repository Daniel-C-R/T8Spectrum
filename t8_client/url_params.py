from datetime import datetime


class UrlParams:
    """
    A class to represent the parameters for a URL.

    Attributes:
    -----------
    host : str
        The host address.
    id : str
        The unique identifier.
    machine : str
        The machine name or identifier.
    point : str
        The point of interest.
    pmode : str
        The mode of operation.
    time : datetime | int
        The time parameter, can be a datetime object or an integer.
    t8_user : str
        The username for T8 authentication.
    t8_password : str
        The password for T8 authentication.

    Methods:
    --------
    __init__(self, host: str, id: str, machine: str, point: str, pmode: str, time:
        datetime | int, t8_user: str, t8_password: str):
        Initializes the UrlParams with the given parameters.
    generate_url(self, info: str) -> str:
        Generates a URL based on the url parameters.
    """

    def __init__(
        self,
        host: str,
        id: str,
        machine: str,
        point: str,
        pmode: str,
        time: datetime | int,
        t8_user: str,
        t8_password: str,
    ):
        self.host = host
        self.id = id
        self.machine = machine
        self.point = point
        self.pmode = pmode
        self.time = time
        self.t8_user = t8_user
        self.t8_password = t8_password

    def generate_url(self, info: str) -> str:
        """
        Generates a URL based on the parameters.

        Args:
        -----
        info : str
            The information to get from the server.

        Returns:
        --------
        str : The generated URL string.
        """
        time = int(self.time.timestamp()) if type(self.time) is datetime else self.time

        return f"https://{self.host}/{self.id}/rest/{info}/{self.machine}/{self.point}/{self.pmode}/{time}"
