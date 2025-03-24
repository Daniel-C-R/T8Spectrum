"""Functions for preprocessing waveforms.

This module provides functions for preprocessing waveforms, including zero padding
and applying a Hanning window.
"""

import numpy as np


def zero_padding(waveform: np.ndarray) -> np.ndarray:
    """Pad the input waveform with zeros to the next power of 2 length.

    Args:
        waveform (np.ndarray): The input waveform array.

    Returns:
        np.ndarray: The zero-padded waveform array with length equal to the next power
            of 2.

    """
    n = len(waveform)
    padded_length = 2 ** np.ceil(np.log2(n)).astype(int)
    return np.pad(waveform, (0, padded_length - n), "constant")


def preprocess_waveform(waveform: np.ndarray) -> np.ndarray:
    """Preprocesses the given waveform by applying a Hanning window and zero padding.

    Args:
        waveform (np.ndarray): The input waveform to preprocess.

    Returns:
        np.ndarray: The preprocessed waveform with a Hanning window applied and zero
            padding.

    """
    windowed_waveform = waveform * np.hanning(len(waveform))
    return zero_padding(windowed_waveform)
