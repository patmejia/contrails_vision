import json
import matplotlib.pyplot as plt
from datetime import datetime

def get_timestamps_from_file(filename):
    """
    Extract timestamps from a given JSON file.
    """
    with open(filename, 'r') as f:
        data = json.load(f)
        timestamps = [entry["timestamp"] for entry in data]
    return timestamps

def convert_to_datetime_format(timestamps):
    """
    Convert a list of timestamps into a datetime format.
    """
    return [datetime.utcfromtimestamp(ts).strftime('%Y-%m') for ts in timestamps]

def plot_histogram(train_dates, validation_dates):
    """
    Plot the histogram for training and validation dates.
    """
    plt.figure(figsize=(15, 6))
    plt.hist(train_dates, bins=30, alpha=0.5, label="Training Dataset", color="blue", edgecolor="black")
    plt.hist(validation_dates, bins=30, alpha=0.5, label="Validation Dataset", color="orange", edgecolor="black")
    plt.title("Temporal Distribution of Training vs. Validation Datasets")
    plt.xlabel("Date")
    plt.ylabel("Number of Records")
    plt.xticks(rotation=45)
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Define the paths to your files
    train_file_path = "samples/opencontrails_mini_sample/train_metadata.json"
    validation_file_path = "samples/opencontrails_mini_sample/validation_metadata.json"

    # Extract timestamps
    train_timestamps = get_timestamps_from_file(train_file_path)
    validation_timestamps = get_timestamps_from_file(validation_file_path)

    # Convert timestamps to datetime format
    train_dates = convert_to_datetime_format(train_timestamps)
    validation_dates = convert_to_datetime_format(validation_timestamps)

    # Check if we have valid data
    if not train_dates and not validation_dates:
        print("No valid months found for both Training and Validation datasets..")
    else:
        plot_histogram(train_dates, validation_dates)
