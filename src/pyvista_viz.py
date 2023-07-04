import pyvista as pv
from pyvista import examples


def download_dataset(dataset_name):
    dataset_functions = {
        'globe': examples.download_topo_global
    }
    return dataset_functions[dataset_name]()

def download_texture(texture_name):
    texture_functions = {
        'globe': examples.load_globe_texture
    }
    return texture_functions[texture_name]()

def compute_normals_and_warp(dataset, factor=0.5e-5):
    # Compute the normals in-place
    dataset.compute_normals(inplace=True)
    # Use those normals to warp the surface
    warp = dataset.warp_by_scalar(factor=factor)
    # Add texture coordinates to the mesh
    warp.texture_map_to_plane(inplace=True)
    return warp

def plot_dataset(dataset, texture=None, cmap="viridis", show_scalar_bar=True):
    p = pv.Plotter()
    p.add_mesh(dataset, texture=texture, cmap=cmap)
    if show_scalar_bar:
        p.show_scalar_bar()
    p.show(interactive=True)

def main():
    dataset = download_dataset('globe')
    warped_dataset = compute_normals_and_warp(dataset)
    # texture = download_texture('globe')
    # plot_dataset(warped_dataset, texture=texture, cmap="gist_earth", show_scalar_bar=False)
    plot_dataset(warped_dataset, cmap="gist_earth", show_scalar_bar=False)

if __name__ == "__main__":
    main()