# PyVista

PyVista provides 3D visualization and mesh analysis tools for Python. Key resources and functionalities include:

#### Visualization Tools

*•* **Renderer**: Utilize the [`Renderer` class](https://docs.pyvista.org/plotting/renderer.html) for 3D scene rendering with `view_isometric()`
*•*  **Surface Normals**: Compute mesh shading and lighting via [surface normals](https://docs.pyvista.org/examples/01-filter/glyphs.html).
*•*  **Point Clouds**: Visualize [point clouds](https://docs.pyvista.org/examples/00-load/create-point-cloud.html) with `add_points()`
*•*  **ITK Plotter**: Employ [ITK plotter](https://docs.pyvista.org/examples/02-plot/itk_plotting.html) for interactive 3D visualization.
*•*  **Time Series**: Visualize [time series data](https://docs.pyvista.org/examples/02-plot/time-series.html) with `add_mesh()`


#### Mesh Analysis Tools

*•*  **Mesh Smoothing**: Smooth meshes with [Laplacian smoothing](https://docs.pyvista.org/examples/01-filter/laplacian_smoothing.html).
*•*  **Mesh Decimation**: Reduce the number of triangles in a mesh with [decimation](https://docs.pyvista.org/examples/01-filter/decimate.html).
*•*  **Mesh Slicing**: Slice meshes with [clipping](https://docs.pyvista.org/examples/01-filter/clip.html).

#### LLA to ECEF Conversion

```python
import pyproj

lla_to_ecef = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
lat, lon, alt = 40, -70, 1000
x, y, z = pyproj.transform(lla_to_ecef, ecef, lon, lat, alt)
print(x, y, z)
```

#### `StructuredGrid` from GOES-16 Data

```python
import xarray as xr
import pyvista as pv

data = xr.open_dataset('path/to/GOES-16-data.nc')
lons, lats, cloud_data = data['lon'].values, data['lat'].values, data['cloud_data'].values
grid = pv.StructuredGrid(lons, lats, cloud_data)
plotter = pv.Plotter()
plotter.add_mesh(grid)
plotter.show()
```

## PyVista Data Visualization Pipeline

### Usage

Follow these steps to utilize the pipeline:

*1.* **Read in the data**:
```python
from netCDF4 import Dataset
data = Dataset('path/to/data.nc')
```
*2.* **Convert radiance to reflectance**:
```python
reflectance = (data.variables['Rad'][:].data * np.pi * 0.3) / 663.274497
```
*3.* **Apply gamma correction**:
```python
gamma_corrected = np.power(reflectance, 0.5)
```
*4.* **Create pseudo-true color images**:
```python
pseudo_true_color = np.dstack((band2, band3, band1))
```
*5.* **Visualize the data using PyVista**:
```python
import pyvista as pv
plotter = pv.Plotter()
plotter.add_mesh(pseudo_true_color)
plotter.show()
```

### Efficient Processing of Large Datasets

#### Chunk Reading for Memory Efficiency
```python
from netCDF4 import Dataset
data = Dataset('path/to/data.nc')
var = data.variables['variable_name']
chunk_size = 1000
n_chunks = var.shape[0] // chunk_size
for i in range(n_chunks):
    start = i * chunk_size
    end = start + chunk_size
    chunk_data = var[start:end]
    # Process the data for this chunk

```

#### Parallelization and Distributed Computing Frameworks
*•*  **Parallelization**: The `multiprocessing` package enables parallel processing of data in chunks. This is useful for CPU-bound tasks such as image processing.
*•*  **Distributed Computing Frameworks**: Dask and Apache Spark distribute data and computation across multiple machines for advanced efficiency.



### Resources and Credits: 

*•* [Brian Blaylock's GOES-16 Download Tool](https://home.chpc.utah.edu/~u0553130/Brian_Blaylock/cgi-bin/goes16_download.cgi)

*•*  [element84/robosat](https://github.com/Element84/robosat-jupyter-notebook/blob/master/Robosat%20Labeling.ipynb)

*•* [Microsoft AI for Earth Datasets, GOES-R Data on GitHub](https://github.com/microsoft/AIforEarthDataSets/blob/main/data/goes-r.md)

*•* [GOES-R Government Official Products Overview](https://www.goes-r.gov/products/overview.html)

*•* [GOES-16 ABI Level 2 Cloud and Moisture Imagery Full Disk Product](https://docs.opendata.aws/noaa-goes16/cics-readme.html)

*•* [NOAA GOES-R Series Advanced Baseline Imager (ABI) Level 2 Cloud and Moisture Imagery Full Disk Product (CMIP/F)](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C01502)