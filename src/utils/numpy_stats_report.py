import os
import numpy as np

def get_files(directory, extension):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                yield os.path.join(root, file)

def compute_stats(data):
    stats = {
        'shape': data.shape,
        'size': data.size,
        'mean': np.mean(data),
        'std_dev': np.std(data),
        'min': np.min(data),
        'max': np.max(data),
        'all_zeros': np.all(data == 0),
        'zero_count': np.count_nonzero(data == 0),  # count of zeros
        'non_zero_count': np.count_nonzero(data)  # count of non-zeros
    }
    return stats

def analyze_data(directory):
    results = []  # Initialize results list
    files_with_zeros = []
    files_without_zeros = []

    for filepath in get_files(directory, ".npy"):
        data = np.load(filepath)
        try:
            stats = compute_stats(data)
            results.append((filepath, stats))  # Append the results

            if stats['zero_count'] > 0:
                files_with_zeros.append(filepath)
            else:
                files_without_zeros.append(filepath)
        except Exception as e:
            print(f"Error processing file {filepath}: {e}")

    return results, files_with_zeros, files_without_zeros  # Return the results list

def generate_markdown_section(title, items):
    section = f'## {title} <a id="{title.lower().replace(" ", "-")}"></a>\n\n'
    for item in items:
        section += f"* {item}\n"
    section += '[Back to ToC](#table-of-contents)\n\n'
    return section

def generate_markdown_report(results, files_with_zeros, files_without_zeros):
    markdown = '## Table of Contents\n\n'
    markdown += '* [File Statistics](#file-statistics)\n'
    markdown += '* [Files with Zeros](#files-with-zeros)\n'
    markdown += '* [Files without Zeros](#files-without-zeros)\n\n'

    # Generate the file statistics section
    markdown += '## File Statistics <a id="file-statistics"></a>\n\n'
    for filepath, stats in results:
        anchor = filepath.replace('.', '').replace('/', '-').replace('_', '-').strip('-')
        markdown += f"### {filepath} <a id='{anchor}'></a>\n\n"
        for stat, value in stats.items():
            markdown += f"* **{stat.capitalize()}**: {value}\n"
        markdown += '[Back to ToC](#table-of-contents)\n\n'

    # Generate the sections for files with and without zeros
    markdown += generate_markdown_section("Files with Zeros", files_with_zeros)
    markdown += generate_markdown_section("Files without Zeros", files_without_zeros)

    return markdown

base_directory = './'
results, files_with_zeros, files_without_zeros = analyze_data(base_directory)
markdown = generate_markdown_report(results, files_with_zeros, files_without_zeros)

# Create directories if they do not exist
os.makedirs('output/numpy_stats', exist_ok=True)

with open('output/numpy_stats/zeros_dataset_report.md', 'w') as f:
    f.write(markdown)
