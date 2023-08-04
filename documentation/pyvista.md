# PyVista Resources

PyVista offers 3D visualization and mesh analysis tools for Python. Below are key resources and code snippets:

- **Renderer**: Utilize the [`Renderer` class](https://docs.pyvista.org/plotting/renderer.html) for 3D scene rendering. Use `view_isometric` for isometric views.
  
- **Surface Normals**: Compute [surface normals](https://docs.pyvista.org/examples/01-filter/glyphs.html) for mesh shading and lighting.
  
- **Point Clouds**: Visualize [point clouds](https://docs.pyvista.org/examples/00-load/create-point-cloud.html) using the `add_points` method.
  
- **ITK Plotter**: Employ the [ITK plotter](https://docs.pyvista.org/examples/02-plot/itk_plotting.html) for interactive 3D visualization.
  
- **Time Series**: Visualize [time series data](https://docs.pyvista.org/examples/02-plot/time-series.html) using the `add_mesh` method.

### Globe Shrinking Example:
```python
from threading import Thread
import time
import numpy as np

def shrink():
    for i in range(50):
        globe.points *= 0.95
        globe.point_data['scalars'] = np.random.rand(globe.n_points)
        time.sleep(0.5)

thread = Thread(target=shrink)
thread.start()
```

### LLA to ECEF Conversion:
```python
import pyproj

lla_to_ecef = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
lat, lon, alt = 40, -70, 1000
x, y, z = pyproj.transform(lla_to_ecef, ecef, lon, lat, alt)
print(x, y, z)
```

### `StructuredGrid` from GOES-16 Data:
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
