import os
import numpy as np
import matplotlib.pyplot as plt

def get_files(directory, extension):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                yield os.path.join(root, file)

def compute_stats(data):
    if data.size > 0:
        cum_mean = np.cumsum(data, dtype=float) / np.arange(1, data.size + 1)
        mean = cum_mean[-1]
    else:
        mean = None

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
        'zero_count': np.count_nonzero(data == 0),  # count of zeros
        'non_zero_count': np.count_nonzero(data),  # count of non-zeros
        'has_nan': np.isnan(data).any(),
        'has_inf': np.isinf(data).any(),
    }
    return stats


def analyze_data(directory):
    results = []
    files_with_zeros = []
    files_without_zeros = []

    for filepath in get_files(directory, ".npy"):
        data = np.load(filepath)
        try:
            stats = compute_stats(data)
            results.append((filepath, stats))

            if stats['zero_count'] > 0:
                files_with_zeros.append(filepath)
            else:
                files_without_zeros.append(filepath)
        except Exception as e:
            print(f"Error processing file {filepath}: {e}")

    return results, files_with_zeros, files_without_zeros

def generate_markdown_section(title, items):
    section = f'## {title}\n\n'
    for item in items:
        section += f"* {item}\n"
    section += '[Back to ToC](#table-of-contents)\n\n'
    return section

def generate_markdown_report(results, files_with_zeros, files_without_zeros):
    markdown = '## Table of Contents\n\n'
    markdown += '* [File Statistics](#file-statistics)\n'
    markdown += '* [Files with Zeros](#files-with-zeros)\n'
    markdown += '* [Files without Zeros](#files-without-zeros)\n\n'

    markdown += '## File Statistics\n\n'
    for filepath, stats in results:
        markdown += f"### {filepath}\n\n"
        for stat, value in stats.items():
            markdown += f"* **{stat.capitalize()}**: {value}\n"
        markdown += '[Back to ToC](#table-of-contents)\n\n'

    markdown += generate_markdown_section("Files with Zeros", files_with_zeros)
    markdown += generate_markdown_section("Files without Zeros", files_without_zeros)

    return markdown

base_directory = './'
results, files_with_zeros, files_without_zeros = analyze_data(base_directory)
markdown = generate_markdown_report(results, files_with_zeros, files_without_zeros)

os.makedirs('output/numpy_stats', exist_ok=True)
with open('output/numpy_stats/zeros_dataset_report.md', 'w') as f:
    f.write(markdown)