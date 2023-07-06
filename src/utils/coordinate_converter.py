import argparse
import os
import numpy as np
import pyvista as pv
import pyproj
from src.main import download_dataset, compute_normals_and_warp, plot_dataset

class CoordinateConverter:
    """Class for converting coordinates from one system to another."""
    def __init__(self):
        self.transformer = pyproj.Transformer.from_crs(
            {"proj":'latlong', "ellps":'WGS84', "datum":'WGS84'}, 
            {"proj":'geocent', "ellps":'WGS84', "datum":'WGS84'}
        )
    
    def lla_to_ecef(self, lat, lon, alt):
        """Converts latitude, longitude, and altitude to earth-centered, earth-fixed (ECEF) coordinates."""
        print(f"Input lat: {lat}")
        print(f"Input lon: {lon}")
        print(f"Input alt: {alt}")
        x, y, z = self.transformer.transform(lon, lat, alt)
        print(f"Output x: {x}")
        print(f"Output y: {y}")
        print(f"Output z: {z}")
        return x, y, z

def parse_args():
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(description='Convert coordinates and visualize data.')
    parser.add_argument('input_dir', type=str, help='Input directory containing npy files.')
    parser.add_argument('output_dir', type=str, help='Output directory to save converted data.')
    return parser.parse_args()

def npy_to_grid(npy_filename):
    """Converts an npy file to a PyVista grid object."""
    data = np.load(npy_filename)
    print(f"Input data: {data}")
    converter = CoordinateConverter()
    x, y, z = converter.lla_to_ecef(data[...,0], data[...,1], data[...,2])
    data_ecef = np.stack((x, y, z), axis=-1)  # stacking arrays along the last axis
    grid = pv.wrap(data_ecef)
    return grid

def main():
    args = parse_args()
    
    for file in os.listdir(args.input_dir):
        if file.endswith('.npy'):
            input_file = os.path.join(args.input_dir, file)
            print(f"Processing file: {input_file}")
            dataset = npy_to_grid(input_file)
            # Extract points from UniformGrid and create a new PolyData object
            points = dataset.points
            polydata_dataset = pv.PolyData(points)
            polydata_dataset["z"] = points[:, 2] # add a new scalar field "z"
            warped_dataset = compute_normals_and_warp(polydata_dataset)
            print(f"First array element: {warped_dataset.points[0]}")
            plot_dataset(warped_dataset, cmap="gist_earth", show_scalar_bar=False)  
    
            # Save transformed dataset to the output directory
            output_file = os.path.join(args.output_dir, file)
            np.save(output_file, warped_dataset)
            print(f"Saved transformed dataset to {output_file}\n")

if __name__ == "__main__":
    main()