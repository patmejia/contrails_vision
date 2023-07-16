import os
import pytest
import pyvista as pv
from pyvista import examples
import matplotlib.pyplot as plt
import main
from unittest.mock import patch, MagicMock

def test_download_dataset():
    with patch.object(examples, 'download_topo_global', return_value=pv.PolyData()):
        dataset = main.download_dataset('globe')
    assert isinstance(dataset, pv.PolyData)

def test_compute_and_warp():
    # Create a dataset with scalars and faces
    points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]]
    faces = [[4, 0, 1, 2, 3]]
    scalars = [1.0, 2.0, 3.0, 4.0]
    dataset = pv.PolyData(points, faces)
    dataset.point_data['scalars'] = scalars

    warped_dataset = main.compute_and_warp(dataset)
    assert isinstance(warped_dataset, pv.PolyData)


def test_create_plotter():
    plotter = main.create_plotter()
    assert isinstance(plotter, pv.Plotter)

def test_add_mesh_to_plotter():
    dataset = pv.PolyData()
    plotter = pv.Plotter()
    with patch.object(plotter, 'add_mesh', return_value=1):
        mesh = main.add_mesh_to_plotter(plotter, dataset, cmap="gist_earth")
    assert mesh == 1

def test_get_output_folder():
    with patch.object(os.path, 'dirname', return_value=''), \
         patch.object(os.path, 'basename', return_value='main.py'), \
         patch.object(os.path, 'join', return_value='output/main'):
        output_folder = main.get_output_folder()
    assert output_folder == 'output/main'

def test_create_output_folder():
    with patch.object(os, 'makedirs') as mock_makedirs, \
         patch.object(os.path, 'exists', return_value=False):
        main.create_output_folder('output/main')
    mock_makedirs.assert_called_once_with('output/main')

def test_save_image():
    plotter = pv.Plotter()
    with patch.object(plotter, 'show', return_value=plt.imread(examples.mapfile)), \
         patch.object(plt, 'imsave'):
        main.save_image(plotter, 'output/main')