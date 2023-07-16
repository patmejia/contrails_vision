import os
import pyvista as pv
from pyvista import examples
import matplotlib.pyplot as plt

DATASET_FUNCTIONS = {'globe': examples.download_topo_global}

def download_dataset(name):
    # Download dataset
    return DATASET_FUNCTIONS[name]()

def compute_and_warp(dataset, factor=0.5e-5):
    # Compute normals and warp
    dataset.compute_normals(inplace=True)
    warp = dataset.warp_by_scalar(factor=factor)
    warp.texture_map_to_plane(inplace=True)
    return warp

def create_plotter():
    # Create plotter
    return pv.Plotter(window_size=(1024, 768), border=True, multi_samples=4)

def add_mesh_to_plotter(plotter, dataset, texture=None, cmap="viridis"):
    # Add mesh to plotter
    return plotter.add_mesh(dataset, texture=texture, cmap=cmap)

def get_output_folder():
    # Get output folder
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    return os.path.join(os.path.dirname(__file__), '..', 'output', script_name)

def create_output_folder(folder):
    # Create output folder
    if not os.path.exists(folder):
        os.makedirs(folder)

def save_image(plotter, folder):
    # Save image
    img = plotter.show(return_img=True)
    plt.imsave(os.path.join(folder, 'tmp.png'), img)

    # Display the image
    plotter.show()

def main():
    dataset = download_dataset('globe')
    warped_dataset = compute_and_warp(dataset)
    plotter = create_plotter()
    add_mesh_to_plotter(plotter, warped_dataset, cmap="gist_earth")
    output_folder = get_output_folder()
    create_output_folder(output_folder)
    save_image(plotter, output_folder)

if __name__ == "__main__":
    main()