import os
from datetime import UTC, datetime

import numpy as np
from dotenv import load_dotenv
from matplotlib import pyplot as plt
from scipy.fft import fft, fftfreq

from t8spectrum.get_data import get_spectra, get_waveform
from t8spectrum.url_params import UrlParams
from t8spectrum.util.plots import plot_waveform
from t8spectrum.waveform import preprocess_waveform

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
    url_params = UrlParams(
        HOST, ID, MACHINE, POINT, PMODE, time_utc, T8_USER, T8_PASSWORD
    )

    waveform, sample_rate = get_waveform(url_params)
    preprocessed_waveform = preprocess_waveform(waveform)

    instants = np.linspace(0, len(waveform) / sample_rate, len(waveform))

    plot_waveform(waveform, sample_rate)

    t8_spectrum, fmin, fmax = get_spectra(url_params)

    t8_freqs = np.linspace(fmin, fmax, len(t8_spectrum))

    # Compute the FFT
    spectrum = fft(preprocessed_waveform)
    spectrum = np.abs(spectrum) / len(spectrum)

    freqs = fftfreq(len(preprocessed_waveform), 1 / sample_rate)

    # Filter the spectrum and frequencies to keep only the range between 50 and 2000 Hz
    mask = (freqs >= fmin) & (freqs <= fmax)
    filtered_spectrum = spectrum[mask]
    filtered_freqs = freqs[mask]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Plot the T8 spectrum
    ax1.plot(t8_freqs, t8_spectrum)
    ax1.set_xlim(fmin, fmax)
    ax1.set_title("T8 Spectrum")
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("Amplitude")
    ax1.grid(True)

    # Plot the computed FFT spectrum
    ax2.plot(filtered_freqs, filtered_spectrum)
    ax2.set_xlim(fmin, fmax)
    ax2.set_title("Computed FFT Spectrum")
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Amplitude")
    ax2.grid(True)

    fig.tight_layout()
    plt.show()
