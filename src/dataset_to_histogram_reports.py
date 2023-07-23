import os
import argparse
import collections
import math
import time
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
        # Calculate basic statistics for the given data
        mean = np.cumsum(data, dtype=float)[-1] / data.size if data.size > 0 else None
        hist, bins = np.histogram(data, bins=50)
        hist = hist.astype(float) / data.size # Normalize histogram

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
            'histogram': (hist, bins)
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
            dataset, record_id = filepath.split('/')[3:5]  # Extract dataset and record id
            results_by_dataset_record[(dataset, record_id)].append((filepath, stats))

        dataset_records = sorted(results_by_dataset_record.keys())
        num_histograms = len(dataset_records)
        num_rows = math.ceil(num_histograms / histograms_per_row)

        fig_band = plt.figure(figsize=(15, num_rows * 7))
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
                
                # Check for new labels
                if os.path.basename(filepath) not in labels_band:
                    labels_band.append(os.path.basename(filepath))
                    patches_band.append(Rectangle((0, 0), 1, 1, fc=color))

            ax_band.set_title(f'Bands for record {record_id} in {dataset}')  
            ax_band.grid(True)

        fig_band.legend(patches_band, labels_band, loc='upper right')
        output_filepath_band = os.path.join(output_dir, 'tiled_bands_histogram.png')
        fig_band.savefig(output_filepath_band)
        plt.close(fig_band)

class ReportGenerator:

    @staticmethod
    def normalize_anchor(text):
        # Convert text to lowercase, replace spaces with hyphens, and remove punctuation
        return text.lower().replace(' ', '-').replace('.', '')

    @staticmethod
    def generate_markdown_for_file(filepath, stats):
        markdown = f"### {filepath}\n\n"
        for stat, value in stats.items():
            markdown += f"- **{stat.capitalize()}**: {value}\n"
        markdown += f'\n[Back to ToC](#{ReportGenerator.normalize_anchor("table of contents")})\n\n'
        return markdown

    @staticmethod
    def generate_markdown_section(title, items):
        section = f'## {title}\n\n'
        for item in items:
            section += f"- {item}\n"
        section += f'\n[Back to ToC](#{ReportGenerator.normalize_anchor("table of contents")})\n\n'
        return section

    @staticmethod
    def save_results(markdown_results, files_with_zeros, files_without_zeros):
        total_files = len(markdown_results)
        total_files_with_zeros = len(files_with_zeros)
        total_files_without_zeros = len(files_without_zeros)
        
        summary = f"## Summary\n\n"
        summary += f"- Total files processed: {total_files}\n"
        summary += f"- Files with zeros: {total_files_with_zeros}\n"
        summary += f"- Files without zeros: {total_files_without_zeros}\n\n"
        
        markdown = '## Table of Contents\n\n'
        markdown += '- [Summary](#summary)\n'
        markdown += summary
        
        for md in markdown_results:
            markdown += md
        
        with open('output/numpy_stats/zeros_dataset_report.md', 'w') as results_file:
            results_file.write(markdown)

class FileProcessor:
    @staticmethod
    def process_file(filepath):
        try:
            data = DataLoader.load_numpy_file(filepath)
            stats = DataAnalyzer.calculate_statistics(data)
            markdown = ReportGenerator.generate_markdown_for_file(filepath, stats)
            return filepath, markdown, stats['zero_count'] > 0, stats
        except Exception as e:
            print(f"Error processing file {filepath}: {e}")
            return None, None, None, None

    @staticmethod
    def process_directory(directory_path):
        files_with_zeros = []
        files_without_zeros = []
        markdown_results = []
        file_stats = {}

        for root, _, files in os.walk(directory_path):
            for file in files:
                filepath = os.path.join(root, file)
                if filepath.endswith('.npy'):
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

def parse_arguments():
    parser = argparse.ArgumentParser(description='Analyze numpy files in a directory.')
    parser.add_argument('directory', type=str, help='The directory to analyze.')
    return parser.parse_args()

def main():
    start_time = time.time()
    args = parse_arguments()
    os.makedirs('output/numpy_stats', exist_ok=True)
    
    file_stats = {}


    try:
        markdown_results, files_with_zeros, files_without_zeros, file_stats = FileProcessor.process_directory(args.directory)
        ReportGenerator.save_results(markdown_results, files_with_zeros, files_without_zeros)
        HistogramGenerator.group_and_plot_histograms_by_dataset_record(file_stats, 'output/numpy_stats', 2) # adjust number of histograms per row here
    except Exception as e:
        print(f"An error occurred: {e}")

    end_time = time.time()
    processed_files_count = len(file_stats)
    print(f"Total time taken: {end_time - start_time:.4f} seconds")
    print(f"Total number of files processed: {processed_files_count}")
    print(f"Processed {processed_files_count / (end_time - start_time):.2f} files per second.")

if __name__ == "__main__":
    main()