import csv
import os

import numpy as np


def save_array_to_csv(file_path: str, array: np.ndarray, column_name: str) -> None:
    """
    Save a NumPy array to a CSV file with a specified column name.

    Parameters:
    file_path (str): The path to the CSV file where the array will be saved.
    array (np.ndarray): The NumPy array to be saved to the CSV file.
    column_name (str): The name of the column to be written as the header in the CSV
    file.

    Returns:
    None
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([column_name])
        for item in array:
            writer.writerow([item])
