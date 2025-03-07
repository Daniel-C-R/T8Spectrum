import os

import numpy as np
from dotenv import load_dotenv
from matplotlib import pyplot as plt

from t8spectrum.get_data import get_spectra, get_waveform

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
    waveform, sample_rate = get_waveform(
        HOST, ID, MACHINE, POINT, PMODE, TIME, T8_USER, T8_PASSWORD
    )

    instants = np.arange(0, len(waveform) / sample_rate, 1 / sample_rate)
    plt.plot(instants, waveform)
    plt.show()

    t8_spectrum = get_spectra(
        HOST, ID, MACHINE, POINT, PMODE, TIME, T8_USER, T8_PASSWORD
    )

    print(t8_spectrum)
    plt.plot(t8_spectrum)
    plt.show()
