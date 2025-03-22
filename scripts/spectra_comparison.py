import numpy as np

from t8_client import get_data
from t8_client.spectrum import calculate_spectrum
from t8_client.util.plots import plot_spectrum_comparison, plot_waveform
from t8_client.waveform import preprocess_waveform

HOST = "lzfs45.mirror.twave.io"
ID = "lzfs45"
MACHINE = "LP_Turbine"
POINT = "MAD31CY005"
PMODE = "AM1"
TIME = "2019-04-11T18:25:54"


def main() -> None:
    t8_user = input("Enter T8 username: ")
    t8_password = input("Enter T8 password: ")

    url_params = {
        "host": HOST,
        "id": ID,
        "machine": MACHINE,
        "point": POINT,
        "pmode": PMODE,
        "time": TIME,
        "t8_user": t8_user,
        "t8_password": t8_password,
    }

    # Get waveform from API
    waveform, sample_rate = get_data.get_wave(**url_params)
    preprocessed_waveform = preprocess_waveform(waveform)

    plot_waveform(waveform, sample_rate)

    # Get T8 spectrum from API
    t8_spectrum, fmin, fmax = get_data.get_spectrum(**url_params)
    t8_freqs = np.linspace(fmin, fmax, len(t8_spectrum))

    # Calculate spectrum from waveform
    filtered_spectrum, filtered_freqs = calculate_spectrum(
        preprocessed_waveform, sample_rate, fmin, fmax
    )

    # Compare T8 spectrum and calculated spectrum
    plot_spectrum_comparison(
        {
            "spectrum1": t8_spectrum,
            "freqs1": t8_freqs,
            "spectrum2": filtered_spectrum,
            "freqs2": filtered_freqs,
            "fmin": fmin,
            "fmax": fmax,
            "title1": "T8 Spectrum",
            "title2": "Calculated Spectrum",
            "xlabel": "Frequency (Hz)",
            "ylabel": "Magnitude",
        }
    )


if __name__ == "__main__":
    main()
