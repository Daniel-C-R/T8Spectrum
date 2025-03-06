import os
from datetime import datetime

from dotenv import load_dotenv

from t8spectrum.get_data import get_waveform

HOST = "lzfs45.mirror.twave.io"
ID = "lzfs45"
MACHINE = "LP_Turbine"
POINT = "MAD31CY005"
PMODE = "AM1"
TIME = 1554907724

load_dotenv()

T8_USER = os.getenv("T8_USER")
T8_PASSWORD = os.getenv("T8_PASSWORD")

if __name__ == "__main__":

    time = datetime.fromtimestamp(TIME)
    waveform = get_waveform(
        HOST, ID, MACHINE, POINT, PMODE, TIME, T8_USER, T8_PASSWORD
    )
    print(waveform)
