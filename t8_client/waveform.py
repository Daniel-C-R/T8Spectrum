import numpy as np


def zero_padding(waveform: np.ndarray):
    """
    Pads the input waveform with zeros to the next power of 2 length.

    Parameters:
    waveform (np.ndarray): The input waveform array.

    Returns:
    np.ndarray: The zero-padded waveform array with length equal to the next power of 2.
    """
    n = len(waveform)
    padded_length = 2 ** np.ceil(np.log2(n)).astype(int)
    return np.pad(waveform, (0, padded_length - n), "constant")


def preprocess_waveform(waveform: np.ndarray):
    """
    Preprocesses the given waveform by applying a Hanning window and zero padding.

    Parameters:
    waveform (np.ndarray): The input waveform to preprocess.

    Returns:
    np.ndarray: The preprocessed waveform with a Hanning window applied and zero
        padding.
    """
    windowed_waveform = waveform * np.hanning(len(waveform))
    return zero_padding(windowed_waveform)
