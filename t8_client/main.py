import os
from datetime import UTC, datetime

import numpy as np
from dotenv import load_dotenv
from get_data import get_spectra, get_waveform
from spectrum import calculate_spectrum
from util.plots import plot_spectrum_comparison, plot_waveform
from waveform import preprocess_waveform

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
    url_params = {
        "host": HOST,
        "id": ID,
        "machine": MACHINE,
        "point": POINT,
        "pmode": PMODE,
        "time": time_utc,
        "t8_user": T8_USER,
        "t8_password": T8_PASSWORD,
    }

    # Get waveform from API
    waveform, sample_rate = get_waveform(**url_params)
    preprocessed_waveform = preprocess_waveform(waveform)

    instants = np.linspace(
        0, len(preprocessed_waveform) / sample_rate, len(preprocessed_waveform)
    )

    plot_waveform(waveform, sample_rate)

    # Get T8 spectrum from API
    t8_spectrum, fmin, fmax = get_spectra(**url_params)
    t8_freqs = np.linspace(fmin, fmax, len(t8_spectrum))

    # Calculate spectrum from waveform
    filtered_spectrum, filtered_freqs = calculate_spectrum(
        preprocessed_waveform, sample_rate, fmin, fmax
    )

    # Compare T8 spectrum and calculated spectrum
    plot_spectrum_comparison(
        t8_spectrum,
        t8_freqs,
        filtered_spectrum,
        filtered_freqs,
        fmin,
        fmax,
        title1="T8 Spectrum",
        title2="Calculated Spectrum",
    )
