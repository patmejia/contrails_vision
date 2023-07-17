import os
import argparse
import collections
import math
import numpy as np
import matplotlib.pyplot as plt


def get_files(directory, extension):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                yield os.path.join(root, file)

def process_directory(directory_path, results, files_with_zeros, files_without_zeros):
    for root, dirs, files in os.walk(directory_path):
        # Ignore the 'test' directory
        dirs[:] = [d for d in dirs if d not in ['test']]
        for file in files:
            filepath = os.path.join(root, file)
            if filepath.endswith('.npy'):  # Only process .npy files
                try:
                    stats = compute_stats(np.load(filepath), filepath)
                    results.append((filepath, stats))
                    if stats['zero_count'] > 0:  # Use 'zero_count' instead of 'zero_values'
                        files_with_zeros.append(filepath)
                    else:
                        files_without_zeros.append(filepath)
                except Exception as e:
                    print(f"Error processing file {filepath}: {str(e)}")

def compute_stats(data, filepath=None):
    if filepath is None:
        filepath_for_filename = 'unknown'
    else:
        filepath_for_filename = filepath.lstrip('./').replace('/', '_')
    
    if data.size > 0:
        cum_mean = np.cumsum(data, dtype=float) / np.arange(1, data.size + 1)
        mean = cum_mean[-1]
        if np.isinf(mean):
            print(f"Warning: Overflow encountered in mean calculation for data from {filepath}.")
            mean = None
    else:
        mean = None
        
    # Calculate histogram
    hist, bins = np.histogram(data, bins=50)
    
    # plot histogram
    fig, ax = plt.subplots()
    ax.bar(bins[:-1], hist, width=np.diff(bins), ec="k", align="edge")
    ax.set_xlabel('Values')  # Set x-axis label
    ax.set_ylabel('Frequency')  # Set y-axis label
    # ax.set_title(f'Histogram for {filepath}')  # Set the title for the histogram
    ax.grid(True)  # Add grid lines
    os.makedirs(os.path.dirname(f'output/numpy_stats/{filepath_for_filename}_histogram.png'), exist_ok=True)
    filename = filepath_for_filename.replace('/', '_')
    plt.savefig(f'output/numpy_stats/{filepath_for_filename}_histogram.png')
    plt.close(fig)

    stats = {
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
    return stats


def analyze_data(base_directory):
    results = []
    files_with_zeros = []
    files_without_zeros = []

    process_directory(base_directory, results, files_with_zeros, files_without_zeros)

    return results, files_with_zeros, files_without_zeros


def generate_markdown_section(title, items):
    section = f'## {title}\n\n'
    for item in items:
        section += f"* {item}\n"
    section += '[Back to ToC](#table-of-contents)\n\n'
    return section

def generate_markdown_report(results, files_with_zeros, files_without_zeros):
    # Generate the summary
    total_files = len(results)
    total_files_with_zeros = len(files_with_zeros)
    total_files_without_zeros = len(files_without_zeros)

    summary = f"""
    ## Summary

    - Total files processed: {total_files}
    - Files with zeros: {total_files_with_zeros}
    - Files without zeros: {total_files_without_zeros}
    """

    # Original report generation code
    markdown = '## Table of Contents\n\n'
    markdown += '* [Summary](#summary)\n'
    markdown += '* [File Statistics](#file-statistics)\n'
    markdown += '* [Files with Zeros](#files-with-zeros)\n'
    markdown += '* [Files without Zeros](#files-without-zeros)\n\n'

    markdown += summary

    markdown += '## File Statistics\n\n'
    for filepath, stats in results:
        markdown += f"### {filepath}\n\n"
        for stat, value in stats.items():
            markdown += f"* **{stat.capitalize()}**: {value}\n"
        #     if stat == 'histogram':
        #         fig, ax = plt.subplots()
        #         ax.bar(value[1][:-1], value[0], width=np.diff(value[1]), ec="k", align="edge")
        #         ax.set_title(f'Histogram for {filepath}')  # Set the title for the histogram
        #         # Replace slashes in the filename with underscores
        #         filename = filepath.replace('/', '_')
        #         plt.savefig(f'output/numpy_stats/{filename}_histogram.png')
        #         plt.close(fig)
        # markdown += '[Back to ToC](#table-of-contents)\n\n'

    markdown += generate_markdown_section("Files with Zeros", files_with_zeros)
    markdown += generate_markdown_section("Files without Zeros", files_without_zeros)

    return markdown


def generate_tiled_histograms(results, output_dir):
    # Group results by dataset and record id 
    results_by_dataset_record = collections.defaultdict(list)
    for filepath, stats in results:
        dataset, record_id = filepath.split('/')[3:5]  # Adjusted to get the correct dataset and record id
        results_by_dataset_record[(dataset, record_id)].append((filepath, stats))
    
    dataset_records = list(results_by_dataset_record.keys())  # Get a list of all dataset-record pairs

    for dataset, record_id in dataset_records:  # Process each dataset-record pair
        record_results = results_by_dataset_record[(dataset, record_id)]
                
        # Separate band and mask results
        band_results = [result for result in record_results if 'band_' in result[0].split('/')[-1]]
        mask_results = [result for result in record_results if 'human_' in result[0].split('/')[-1]]

        # Plot band histograms
        fig, ax = plt.subplots(figsize=(12, 6))  # Create a new figure for each record
        for filepath, stats in band_results:
            hist, bins = stats['histogram']
            ax.bar(bins[:-1], hist, width=np.diff(bins), ec="k", align="edge", alpha=0.5, label=os.path.basename(filepath))
        
        ax.set_title(f'Bands for record {record_id} in {dataset}')  # Add title to band histograms
        ax.grid(True)  # Add grid lines
        ax.legend()  # Add legend

        # Save the figure
        output_filepath = os.path.join(output_dir, f'{dataset}_record_{record_id}_bands_histogram.png')
        fig.savefig(output_filepath)
        plt.close(fig)

        # Plot mask histograms
        fig, ax = plt.subplots(figsize=(12, 6))  # Create a new figure for each record
        for filepath, stats in mask_results:
            hist, bins = stats['histogram']
            ax.bar(bins[:-1], hist, width=np.diff(bins), ec="k", align="edge", alpha=0.5, label=os.path.basename(filepath))
        
        ax.set_title(f'Masks for record {record_id} in {dataset}')  # Add title to mask histograms
        ax.grid(True)  # Add grid lines
        ax.legend()  # Add legend

        # Save the figure
        output_filepath = os.path.join(output_dir, f'{dataset}_record_{record_id}_masks_histogram.png')
        fig.savefig(output_filepath)
        plt.close(fig)


# define the command-line arguments
parser = argparse.ArgumentParser(description='Analyze numpy files in a directory.')
parser.add_argument('directory', type=str, help='The directory to analyze.')

# parse the command-line arguments
args = parser.parse_args()

# use the directory provided in the command-line arguments
base_directory = args.directory
results, files_with_zeros, files_without_zeros = analyze_data(base_directory)
markdown = generate_markdown_report(results, files_with_zeros, files_without_zeros)

os.makedirs('output/numpy_stats', exist_ok=True)
with open('output/numpy_stats/zeros_dataset_report.md', 'w') as f:
    f.write(markdown)
    
# Call the new function to generate tiled histograms
generate_tiled_histograms(results, 'output/numpy_stats')