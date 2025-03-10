import os
from datetime import UTC, datetime

import numpy as np
from dotenv import load_dotenv
from matplotlib import pyplot as plt

from t8spectrum.get_data import get_spectra, get_waveform
from t8spectrum.util.plots import plot_waveform

HOST = "lzfs45.mirror.twave.io"
ID = "lzfs45"
MACHINE = "LP_Turbine"
POINT = "MAD31CY005"
PMODE = "AM1"
TIME = "11-04-2019 18:25:54"

load_dotenv()

T8_USER = os.getenv("T8_USER")
T8_PASSWORD = os.getenv("T8_PASSWORD")

if __name__ == "__main__":
    time_utc = datetime.strptime(TIME, "%d-%m-%Y %H:%M:%S").replace(tzinfo=UTC)

    waveform, sample_rate = get_waveform(
        HOST, ID, MACHINE, POINT, PMODE, time_utc, T8_USER, T8_PASSWORD
    )

    instants = np.linspace(0, len(waveform) / sample_rate, len(waveform))

    plot_waveform(waveform, sample_rate)

    t8_spectrum, fmin, fmax = get_spectra(
        HOST, ID, MACHINE, POINT, PMODE, time_utc, T8_USER, T8_PASSWORD
    )

    t8_freqs = np.linspace(fmin, fmax, len(t8_spectrum))

    plt.plot(t8_freqs, t8_spectrum)
    plt.grid(True)
    plt.show()
