"""Module for calculating the spectrum of a waveform."""

import numpy as np
from scipy.fft import fft, fftfreq


def calculate_spectrum(
    waveform: np.ndarray, sample_rate: float, fmin: float, fmax: float
) -> tuple[np.ndarray, np.ndarray]:
    """Calculate the spectrum of a waveform.

    Calculate the frequency spectrum of a given waveform within a specified frequency
    range.

    Args:
        waveform (np.ndarray): The input signal waveform.
        sample_rate (float): The sampling rate of the waveform in Hz.
        fmin (float): The minimum frequency of interest in Hz.
        fmax (float): The maximum frequency of interest in Hz.

    Returns:
        tuple[np.ndarray, np.ndarray]: A tuple containing:
            - filtered_spectrum (np.ndarray): The magnitude of the frequency spectrum
                within the specified range, with an RMS AC detector.
            - filtered_freqs (np.ndarray): The corresponding frequencies within the
                specified range.

    """
    spectrum = fft(waveform) * 2 * np.sqrt(2)
    magintude = np.abs(spectrum) / len(spectrum)
    freqs = fftfreq(len(waveform), 1 / sample_rate)
    filtered_spectrum = magintude[(freqs >= fmin) & (freqs <= fmax)]
    filtered_freqs = freqs[(freqs >= fmin) & (freqs <= fmax)]
    return filtered_spectrum, filtered_freqs
