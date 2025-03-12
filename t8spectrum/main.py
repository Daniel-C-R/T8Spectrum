import os
from datetime import UTC, datetime

import numpy as np
from dotenv import load_dotenv
from matplotlib import pyplot as plt
from scipy.fft import rfft

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

    plt.plot(t8_spectrum)
    plt.xlim(fmin, fmax)
    plt.grid(True)
    plt.show()

    # Apply a Hanning window
    windowed_waveform = waveform * np.hanning(len(waveform))

    # Zero padding to the next power of 2
    n = len(windowed_waveform)
    padded_length = 2 ** np.ceil(np.log2(n)).astype(int)
    padded_waveform = np.pad(windowed_waveform, (0, padded_length - n), "constant")

    # Compute the FFT
    spectrum = rfft(padded_waveform)

    plt.plot(spectrum)
    plt.xlim(fmin, fmax)
    plt.grid(True)
    plt.show()
