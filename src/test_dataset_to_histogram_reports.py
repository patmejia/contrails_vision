import os
import shutil
import pytest
import numpy as np
from dataset_to_histogram_reports import DataLoader, DataAnalyzer, HistogramGenerator, ReportGenerator, FileProcessor

def test_data_loader():
    test_data = np.array([1, 2, 3])
    np.save('test.npy', test_data)
    loaded_data = DataLoader.load_numpy_file('test.npy')
    assert np.array_equal(test_data, loaded_data)

def test_data_analyzer():
    test_data = np.array([1, 2, 3])
    stats = DataAnalyzer.calculate_statistics(test_data)
    assert stats['mean'] == 2
    assert stats['std_dev'] == np.std(test_data)
    assert stats['min'] == 1
    assert stats['max'] == 3
    assert stats['median'] == 2
    assert stats['all_zeros'] == False
    assert stats['zero_count'] == 0
    assert stats['non_zero_count'] == 3
    assert stats['has_nan'] == False
    assert stats['has_inf'] == False

def test_histogram_generator():
    hist = np.array([1, 2, 3])
    bins = np.array([0, 1, 2, 3])
    output_dir = "test_dir"
    os.makedirs(output_dir, exist_ok=True)
    HistogramGenerator.save_histogram(hist, bins, os.path.join(output_dir, 'test.png'))
    assert os.path.isfile(os.path.join(output_dir, 'test.png'))
    shutil.rmtree(output_dir) # cleanup

def test_report_generator():
    stats = {'mean': 2, 'std_dev': 1, 'min': 1, 'max': 3, 'median': 2}
    markdown = ReportGenerator.generate_markdown_for_file('test.npy', stats)
    print(markdown)  # Print the generated markdown
    assert '### test.npy' in markdown
    assert "- **Mean**: 2" in markdown if markdown else False

def test_file_processor():
    test_data = np.array([1, 2, 3])
    np.save('test.npy', test_data)
    filepath, markdown, has_zeros, stats = FileProcessor.process_file('test.npy')
    print(markdown)  # Print the generated markdown
    assert filepath == 'test.npy'
    assert "- **Mean**: 2" in markdown if markdown else False
    assert has_zeros == False
    if stats:  # Ensure stats is not None before accessing elements
        assert stats['mean'] == 2
    else:
        assert False    


