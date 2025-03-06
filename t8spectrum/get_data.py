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
    if type(time) is datetime:
        time = time.timestamp()

    url = f"https://{host}/{id}/rest/waves/{machine}/{point}/{pmode}/{time}"
    response = requests.get(url, auth=(t8_user, t8_password))
    if response.status_code != 200:
        raise Exception(f"Failed to get waveform: {response.text}")

    waveform = zint_to_float(response.json()["data"])
    sample_rate = response.json()["sample_rate"]

    return waveform, sample_rate
