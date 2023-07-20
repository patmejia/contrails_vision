import os
import argparse
import collections
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.patches import Rectangle

class DataLoader:
    @staticmethod
    def load_numpy_file(filepath):
        return np.load(filepath)

class DataAnalyzer:
    @staticmethod
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

class HistogramGenerator:
    @staticmethod
    def save_histogram(hist, bins, output_path):
        fig, ax = plt.subplots()
        ax.set_xlabel('Values')
        ax.set_ylabel('Frequency')
        ax.grid(True)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path)
        plt.close(fig)
    
    @staticmethod
    def group_and_plot_histograms_by_dataset_record(file_stats, output_dir, histograms_per_row):
        results_by_dataset_record = collections.defaultdict(list)
        
        for filepath, stats in file_stats.items():
            dataset, record_id = filepath.split('/')[3:5]  # Adjust to correct dataset and record id
            results_by_dataset_record[(dataset, record_id)].append((filepath, stats))

        dataset_records = list(results_by_dataset_record.keys())  # Get a list of all dataset-record pairs
        dataset_records.sort()
        num_histograms = len(dataset_records)
        num_rows = math.ceil(num_histograms / histograms_per_row)

        # Create a separate figure for the band histograms
        fig_band = plt.figure(figsize=(15, num_rows * 7))

        # Create empty lists for the legend patches and labels
        patches_band = []
        labels_band = []

        for i, (dataset, record_id) in enumerate(dataset_records):
            record_results = results_by_dataset_record[(dataset, record_id)]
            band_results = [result for result in record_results if 'band_' in result[0].split('/')[-1]]
            colors_band = cm.viridis(np.linspace(0, 1, len(band_results)))  # type: ignore

            ax_band = fig_band.add_subplot(num_rows, histograms_per_row, i+1)
            for color, (filepath, stats) in zip(colors_band, band_results):
                hist, bins = stats['histogram']
                ax_band.bar(bins[:-1], hist, width=np.diff(bins), ec="k", align="edge", alpha=0.5, color=color)
                patches_band.append(Rectangle((0, 0), 1, 1, fc=color))
                labels_band.append(os.path.basename(filepath))

            ax_band.set_title(f'Bands for record {record_id} in {dataset}')  
            ax_band.grid(True)

        # Create a single legend for the entire band figure
        fig_band.legend(patches_band, labels_band, loc='upper right')

        output_filepath_band = os.path.join(output_dir, f'tiled_bands_histogram.png')
        fig_band.savefig(output_filepath_band)
        plt.close(fig_band)

        # Create a separate figure for the mask histograms
        fig_mask = plt.figure(figsize=(15, num_rows * 7))

        # Create empty lists for the legend patches and labels
        patches_mask = []
        labels_mask = []

        for i, (dataset, record_id) in enumerate(dataset_records):
            record_results = results_by_dataset_record[(dataset, record_id)]
            mask_results = [result for result in record_results if 'human_' in result[0].split('/')[-1]]
            colors_mask = cm.viridis(np.linspace(0, 1, len(mask_results)))  # type: ignore

            ax_mask = fig_mask.add_subplot(num_rows, histograms_per_row, i+1)
            for color, (filepath, stats) in zip(colors_mask, mask_results):
                hist, bins = stats['histogram']
                ax_mask.bar(bins[:-1], hist, width=np.diff(bins), ec="k", align="edge", alpha=0.5, color=color)
                patches_mask.append(Rectangle((0, 0), 1, 1, fc=color))
                labels_mask.append(os.path.basename(filepath))

            ax_mask.set_title(f'Masks for record {record_id} in {dataset}')  
            ax_mask.grid(True)

        # Create a single legend for the entire mask figure
        fig_mask.legend(patches_mask, labels_mask, loc='upper right')

        output_filepath_mask = os.path.join(output_dir, f'tiled_masks_histogram.png')
        fig_mask.savefig(output_filepath_mask)
        plt.close(fig_mask)
    pass

class ReportGenerator:
    @staticmethod
    def generate_markdown_for_file(filepath, stats):
        markdown = f"### {filepath}\n\n"
        for stat, value in stats.items():
            markdown += f"* **{stat.capitalize()}**: {value}\n"
        markdown += '[Back to ToC](#table-of-contents)\n\n'
        return markdown

    @staticmethod
    def generate_markdown_section(title, items):
        section = f'## {title}\n\n'
        for item in items:
            section += f"* {item}\n"
        section += '[Back to ToC](#table-of-contents)\n\n'
        return section

    @staticmethod
    def save_results(markdown_results, files_with_zeros, files_without_zeros):
        with open('output/numpy_stats/zeros_dataset_report.md', 'w') as results_file:
            for markdown in markdown_results:
                results_file.write(markdown)
            results_file.write(ReportGenerator.generate_markdown_section("Files with Zeros", files_with_zeros))
            results_file.write(ReportGenerator.generate_markdown_section("Files without Zeros", files_without_zeros))

class FileProcessor:
    @staticmethod
    def process_file(filepath):
        try:
            data = DataLoader.load_numpy_file(filepath)
            stats = DataAnalyzer.calculate_statistics(data)
            markdown = ReportGenerator.generate_markdown_for_file(filepath, stats)
            has_zeros = stats['zero_count'] > 0
            return filepath, markdown, has_zeros, stats
        except Exception as e:
            print(f"Error processing file {filepath}: {str(e)}")
            return None, None, None, None

    @staticmethod
    def process_directory(directory_path):
        files_with_zeros = []
        files_without_zeros = []
        markdown_results = []
        file_stats = {}

        for root, dirs, files in os.walk(directory_path):
            dirs[:] = [d for d in dirs if d not in ['test']] # Adjust: Ignore the test directory
            for file in files:
                filepath = os.path.join(root, file)
                if filepath.endswith('.npy'):  # Only process .npy files
                    filepath, markdown, has_zeros, stats = FileProcessor.process_file(filepath)
                    if filepath is None:
                        continue
                    if has_zeros:
                        files_with_zeros.append(filepath)
                    else:
                        files_without_zeros.append(filepath)
                    markdown_results.append(markdown)
                    file_stats[filepath] = stats

        return markdown_results, files_with_zeros, files_without_zeros, file_stats

# Parse arguments from command line
def parse_arguments():
    parser = argparse.ArgumentParser(description='Analyze numpy files in a directory.')
    parser.add_argument('directory', type=str, help='The directory to analyze.')
    return parser.parse_args()

# Main function to handle the overall process
def main():
    args = parse_arguments()
    base_directory = args.directory
    os.makedirs('output/numpy_stats', exist_ok=True)

    try:
        markdown_results, files_with_zeros, files_without_zeros, file_stats = FileProcessor.process_directory(base_directory)
        ReportGenerator.save_results(markdown_results, files_with_zeros, files_without_zeros)

        # Pass the file_stats dictionary to the histogram function
        HistogramGenerator.group_and_plot_histograms_by_dataset_record(file_stats, 'output/numpy_stats', 2) # n histograms per row
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()