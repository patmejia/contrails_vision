import pytest
import numpy as np
import os

# Import your functions here
from dataset_to_histogram_reports import load_numpy_file, calculate_statistics, process_file

def test_load_numpy_file(tmp_path):
    # Create a temporary numpy file
    p = tmp_path / "temp.npy"
    np.save(p, np.array([1, 2, 3, 4, 5]))
    
    # Test load_numpy_file function
    data = load_numpy_file(p)
    assert np.array_equal(data, np.array([1, 2, 3, 4, 5]))

def test_calculate_statistics():
    data = np.array([1, 2, 3, 4, 5])
    
    # Test calculate_statistics function
    stats = calculate_statistics(data)
    
    assert stats['shape'] == data.shape
    assert stats['size'] == data.size
    assert stats['mean'] == np.mean(data)
    assert stats['std_dev'] == np.std(data)
    assert stats['min'] == np.min(data)
    assert stats['max'] == np.max(data)
    assert stats['median'] == np.median(data)
    assert stats['all_zeros'] == np.all(data == 0)
    assert stats['zero_count'] == np.count_nonzero(data == 0)
    assert stats['non_zero_count'] == np.count_nonzero(data)
    assert stats['has_nan'] == np.isnan(data).any()
    assert stats['has_inf'] == np.isinf(data).any()

def test_process_file(tmp_path):
    # Create a temporary numpy file
    p = tmp_path / "temp.npy"
    np.save(p, np.array([1, 2, 3, 4, 5]))
    
    # Test process_file function
    filepath, markdown, has_zeros = process_file(p)
    
    assert str(filepath) == str(p)
    assert markdown is not None
    assert has_zeros == False
