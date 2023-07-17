import os
import warnings
import argparse
import collections
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import viridis



def load_numpy_file(filepath):
    return np.load(filepath)

def calculate_statistics(data):
    mean = np.cumsum(data, dtype=float)[-1] / data.size if data.size > 0 else None
    hist, bins = np.histogram(data, bins=50)
    hist = hist / data.size  # Normalize histogram

    return {
        'shape': data.shape,
        'size': data.size,
        'mean': mean,
        'std_dev': np.std(data),
        'min': np.min(data),
        'max': np.max(data),
        'median': np.median(data),
        'percentiles': np.percentile(data, [25, 50, 75]) if data.size > 0 else [None, None, None],
        'all_zeros': np.all(data == 0),
        'zero_count': np.count_nonzero(data == 0),
        'non_zero_count': np.count_nonzero(data),
        'has_nan': np.isnan(data).any(),
        'has_inf': np.isinf(data).any(),
        'histogram': (hist, bins)  # Add the histogram data
    }

def save_histogram(hist, bins, output_path):
    fig, ax = plt.subplots()
    # ax.bar(bins[:-1], hist, width=np.diff(bins), ec="k", align="edge")
    ax.set_xlabel('Values')
    ax.set_ylabel('Frequency')
    ax.grid(True)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close(fig)

def generate_markdown_for_file(filepath, stats):
    markdown = f"### {filepath}\n\n"
    for stat, value in stats.items():
        markdown += f"* **{stat.capitalize()}**: {value}\n"
    markdown += '[Back to ToC](#table-of-contents)\n\n'
    return markdown

def process_file(filepath):
    try:
        data = load_numpy_file(filepath)
        stats = calculate_statistics(data)
        # hist, bins = stats['histogram'] # Unpack histogram data
        # output_path = f'output/numpy_stats/{os.path.basename(filepath)}_histogram.png'
        # save_histogram(hist, bins, output_path) # Call the function with separate arguments
        return filepath, generate_markdown_for_file(filepath, stats), stats['zero_count'] > 0
    except Exception as e:
        print(f"Error processing file {filepath}: {str(e)}")
        return None, None, None


def process_directory(directory_path):
    files_with_zeros = []
    files_without_zeros = []
    markdown_results = []

    for root, dirs, files in os.walk(directory_path):
        dirs[:] = [d for d in dirs if d not in ['test']] # Ignore the test directory
        for file in files:
            filepath = os.path.join(root, file)
            if filepath.endswith('.npy'):  # Only process .npy files
                filepath, markdown, has_zeros = process_file(filepath)
                if filepath is None:
                    continue
                if has_zeros:
                    files_with_zeros.append(filepath)
                else:
                    files_without_zeros.append(filepath)
                markdown_results.append(markdown)

    return markdown_results, files_with_zeros, files_without_zeros


def generate_markdown_section(title, items):
    section = f'## {title}\n\n'
    for item in items:
        section += f"* {item}\n"
    section += '[Back to ToC](#table-of-contents)\n\n'
    return section

def save_results(markdown_results, files_with_zeros, files_without_zeros):
    with open('output/numpy_stats/zeros_dataset_report.md', 'w') as results_file:
        for markdown in markdown_results:
            results_file.write(markdown)
        results_file.write(generate_markdown_section("Files with Zeros", files_with_zeros))
        results_file.write(generate_markdown_section("Files without Zeros", files_without_zeros))


def group_and_plot_histograms_by_dataset_record(directory_path, output_dir, histograms_per_row):
    # Group results by dataset and record id 
    results_by_dataset_record = collections.defaultdict(list)
    for root, dirs, files in os.walk(directory_path):
        # dirs[:] = [d for d in dirs if d not in ['test']]
        for file in files:
            filepath = os.path.join(root, file)
            if filepath.endswith('.npy'):  # Only process .npy files
                data = np.load(filepath)
                stats = calculate_statistics(data)
                dataset, record_id = filepath.split('/')[3:5]  # Adjusted to get the correct dataset and record id
                results_by_dataset_record[(dataset, record_id)].append((filepath, stats))
    
    dataset_records = list(results_by_dataset_record.keys())  # Get a list of all dataset-record pairs

    # Sort the dataset records by dataset type and record id
    dataset_records.sort()

    # Calculate the number of rows and columns for the tiled plot
    num_histograms = len(dataset_records)
    num_rows = math.ceil(num_histograms / histograms_per_row)

    # Create a new figure
    fig = plt.figure(figsize=(15, num_rows * 7))

    for i, (dataset, record_id) in enumerate(dataset_records):  # Process each dataset-record pair
        record_results = results_by_dataset_record[(dataset, record_id)]
                
        # Separate band and mask results
        band_results = [result for result in record_results if 'band_' in result[0].split('/')[-1]]
        mask_results = [result for result in record_results if 'human_' in result[0].split('/')[-1]]

        # Create color palette for band histograms
        colors = viridis(np.linspace(0, 1, len(band_results)))

        # Add a new subplot for the band histograms
        ax = fig.add_subplot(num_rows, histograms_per_row, i+1)
        for color, (filepath, stats) in zip(colors, band_results):
            hist, bins = stats['histogram']
            ax.bar(bins[:-1], hist, width=np.diff(bins), ec="k", align="edge", alpha=0.5, label=os.path.basename(filepath), color=color)

        ax.set_title(f'Bands for record {record_id} in {dataset}')  # Add title to band histograms
        ax.grid(True)  # Add grid lines

        labels = [os.path.basename(filepath) for filepath, _ in band_results]
        ax.legend(labels, loc='upper left', bbox_to_anchor=(1, 1))  # Set labels explicitly when calling legend

    # Save the figure
    output_filepath = os.path.join(output_dir, f'tiled_bands_histogram.png')
    fig.savefig(output_filepath)
    plt.close(fig)

    fig = plt.figure(figsize=(15, num_rows * 7))
    for i, (dataset, record_id) in enumerate(dataset_records):  # Process each dataset-record pair
        record_results = results_by_dataset_record[(dataset, record_id)]

        # Separate band and mask results
        band_results = [result for result in record_results if 'band_' in result[0].split('/')[-1]]
        mask_results = [result for result in record_results if 'human_' in result[0].split('/')[-1]]

        # Create color palette for mask histograms
        colors = viridis(np.linspace(0, 1, len(mask_results)))

        # Add a new subplot for the mask histograms
        ax = fig.add_subplot(num_rows, histograms_per_row, i+1)
        for color, (filepath, stats) in zip(colors, mask_results):
            hist, bins = stats['histogram']
            ax.bar(bins[:-1], hist, width=np.diff(bins), ec="k", align="edge", alpha=0.5, label=os.path.basename(filepath), color=color)

        ax.set_title(f'Masks for record {record_id} in {dataset}')  # Add title to mask histograms
        ax.grid(True)  # Add grid lines

        labels = [os.path.basename(filepath) for filepath, _ in mask_results]
        ax.legend(labels, loc='upper left', bbox_to_anchor=(1, 1))  # Set labels explicitly when calling legend
                
    # Save the figure
    output_filepath = os.path.join(output_dir, f'tiled_masks_histogram.png')
    fig.savefig(output_filepath)
    plt.close(fig)



def parse_arguments():
    parser = argparse.ArgumentParser(description='Analyze numpy files in a directory.')
    parser.add_argument('directory', type=str, help='The directory to analyze.')
    return parser.parse_args()

def main():
    args = parse_arguments()
    base_directory = args.directory
    os.makedirs('output/numpy_stats', exist_ok=True)

    try:
        markdown_results, files_with_zeros, files_without_zeros = process_directory(base_directory)
        save_results(markdown_results, files_with_zeros, files_without_zeros)

        # Call the new function to generate tiled histograms
        group_and_plot_histograms_by_dataset_record(base_directory, 'output/numpy_stats', 2) # n histograms per row
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()