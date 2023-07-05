import os
import pyvista as pv
from pyvista import examples


def download_dataset(dataset_name):
    dataset_functions = {
        'globe': examples.download_topo_global
    }
    return dataset_functions[dataset_name]()

def compute_normals_and_warp(dataset, factor=0.5e-5):
    dataset.compute_normals(inplace=True)
    warp = dataset.warp_by_scalar(factor=factor)
    warp.texture_map_to_plane(inplace=True)
    return warp

def plot_dataset(dataset, texture=None, cmap="viridis", show_scalar_bar=True):
    p = pv.Plotter(off_screen=True, notebook=False, window_size=(1024, 768), border=True, multi_samples=4)
    mesh = p.add_mesh(dataset, texture=texture, cmap=cmap, scalar_bar_args=None)
    if show_scalar_bar:
        p.add_scalar_bar(mesh, title="Elevation [m]")
    output_folder = os.path.join(os.path.dirname(__file__), '..', 'output')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    p.show()
    p.screenshot(os.path.join(output_folder, 'tmp.png'))


def main():
    dataset = download_dataset('globe')
    warped_dataset = compute_normals_and_warp(dataset)
    plot_dataset(warped_dataset, cmap="gist_earth", show_scalar_bar=False)  
    
if __name__ == "__main__":
    main()