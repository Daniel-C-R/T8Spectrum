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
