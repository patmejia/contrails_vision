import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import pytest
import pyvista as pv
from pyvista import examples
from main import download_dataset, compute_normals_and_warp, plot_dataset


def test_download_dataset():
    dataset = download_dataset('globe')
    assert isinstance(dataset, pv.PolyData)


def test_compute_normals_and_warp():
    dataset = examples.download_topo_global()
    warped_dataset = compute_normals_and_warp(dataset)
    assert isinstance(warped_dataset, pv.PolyData)


def test_plot_dataset(mocker):
    dataset = examples.download_topo_global()
    warped_dataset = compute_normals_and_warp(dataset)

    # Mock the Plotter
    mocker.patch('pyvista.Plotter')
    mock_plotter = pv.Plotter()

    plot_dataset(warped_dataset, cmap="gist_earth", show_scalar_bar=False)

    # Check that methods were called on the mock Plotter
    mock_plotter.add_mesh.assert_called_once()
    mock_plotter.show.assert_called_once()


if __name__ == "__main__":
    pytest.main()
