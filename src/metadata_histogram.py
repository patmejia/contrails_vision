import json
import os
import matplotlib.pyplot as plt
from datetime import datetime

def load_json_file(filename):
    # Load JSON from a file
    with open(filename, 'r') as f:
        return json.load(f)

def get_timestamps(data):
    # Extract timestamps from data
    return [entry["timestamp"] for entry in data]

def to_datetime_format(timestamps):
    # Convert timestamps to datetime
    return [datetime.utcfromtimestamp(ts).strftime('%Y-%m') for ts in timestamps]

def plot_and_save_histogram(train_dates, validation_dates, save_path=None):
    # Plot histogram and save
    plt.figure(figsize=(15, 6))
    plt.hist(train_dates, bins=30, alpha=0.5, label="Training Dataset", color="blue", edgecolor="black")
    plt.hist(validation_dates, bins=30, alpha=0.5, label="Validation Dataset", color="orange", edgecolor="black")
    plt.title("Temporal Distribution of Training vs. Validation Datasets")
    plt.xlabel("Date")
    plt.ylabel("Number of Records")
    plt.xticks(rotation=45)
    plt.legend(loc="upper left")
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to: {save_path}")

    plt.show()

def ensure_dir_exists(directory):
    # Create directory if not exists
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():
    # Paths
    train_file_path = "samples/opencontrails_mini_sample/train_metadata.json"
    validation_file_path = "samples/opencontrails_mini_sample/validation_metadata.json"

    # Load data and convert timestamps
    train_dates = to_datetime_format(get_timestamps(load_json_file(train_file_path)))
    validation_dates = to_datetime_format(get_timestamps(load_json_file(validation_file_path)))

    if not train_dates and not validation_dates:
        print("No valid months found for datasets.")
        return

    # Directories setup
    output_dir = "output"
    script_name_dir = os.path.splitext(os.path.basename(__file__))[0]
    full_dir_path = os.path.join(output_dir, script_name_dir)
    ensure_dir_exists(full_dir_path)

    # Plot and save histogram
    plot_filename = os.path.join(full_dir_path, "train_vs_validation_distribution.png")
    plot_and_save_histogram(train_dates, validation_dates, save_path=plot_filename)

if __name__ == "__main__":
    main()