import numpy as np
from matplotlib import pyplot as plt


def plot_waveform(waveform, sample_rate):
    """
    Plots a waveform.

    Args:
        waveform (np.ndarray): The waveform to plot.
        sample_rate (int): The sample rate of the waveform.
    """
    instants = np.linspace(0, len(waveform) / sample_rate, len(waveform))

    plt.plot(instants, waveform)
    plt.grid(True)
    plt.show()


def plot_spectrum_comparison(
    spectrum1: np.ndarray,
    freqs1: np.ndarray,
    spectrum2: np.ndarray,
    freqs2: np.ndarray,
    fmin: float,
    fmax: float,
    title1: str = "Spectrum 1",
    title2: str = "Spectrum 2",
    xlabel: str = "Frequency (Hz)",
    ylabel: str = "Amplitude",
):
    """
    Plots a comparison of two spectra.

    Args:
        spectrum1 (np.ndarray): The first spectrum to plot.
        freqs1 (np.ndarray): The frequencies corresponding to the first spectrum.
        spectrum2 (np.ndarray): The second spectrum to plot.
        freqs2 (np.ndarray): The frequencies corresponding to the second spectrum.
        fmin (float): The minimum frequency to plot.
        fmax (float): The maximum frequency to plot.
        title1 (str): The title of the first spectrum plot.
        title2 (str): The title of the second spectrum plot.
        xlabel (str): The label for the x-axis.
        ylabel (str): The label for the y-axis.
    """
    _, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    ax1.plot(freqs1, spectrum1)
    ax1.set_xlim(fmin, fmax)
    ax1.set_title(title1)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax1.grid(True)

    ax2.plot(freqs2, spectrum2)
    ax2.set_xlim(fmin, fmax)
    ax2.set_title(title2)
    ax2.set_xlabel(xlabel)
    ax2.set_ylabel(ylabel)
    ax2.grid(True)

    plt.tight_layout()
    plt.show()
