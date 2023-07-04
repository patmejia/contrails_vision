# pyvista resources


### `pyvista.Renderer.view_isometric`

#### [surface normals](https://docs.pyvista.org/version/stable/examples/01-filter/compute-normals.html#sphx-glr-download-examples-01-filter-compute-normals-py)

#### [point clounds](https://docs.pyvista.org/version/stable/examples/00-load/create-point-cloud.html)

#### [point could, ITK plotter for interactivity examples](https://topogenesis.readthedocs.io/notebooks/point_cloud_voxelization/)

#### [time series](https://docs.pyvista.org/version/stable/api/plotting/plotting.html)
```python
# shrink globe in the background
def shrink():
    for i in range(50):
        globe.points *= 0.95
        # Update scalars
        globe.point_data['scalars'] = np.random.rand(globe.n_points)
        time.sleep(0.5)

thread = Thread(target=shrink)
thread.start()
```

#### [a try at MRI slicing with pyvista](https://www.codeproject.com/Questions/5342943/How-to-accelerate-MRI-slicing-using-pyvista)

#### time series: https://docs.pyvista.org/version/stable/api/plotting/plotting.html

#### [detection, collision](https://docs.pyvista.org/version/stable/examples/01-filter/collisions.html)

The conversion from Latitude, Longitude, Altitude (LLA) to Earth Centered Earth Fixed (ECEF) coordinates is a common requirement in geospatial work. This conversion can be performed using the pyproj library in Python:

```bash
pip install pyproj
```

convert LLA to ECEF coordinates using the `pyproj` library:

```python
import pyproj

# Initialize the conversion functions
lla_to_ecef = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')

# Define a latitude, longitude, and altitude (LLA)
lat, lon, alt = 40, -70, 1000  # in degrees and meters

# Convert LLA to ECEF
x, y, z = pyproj.transform(lla_to_ecef, ecef, lon, lat, alt)

print(x, y, z)
```

In this example, `x`, `y`, and `z` are the ECEF coordinates in meters. Note that this example uses the WGS84 ellipsoid, which is the standard choice for much of modern geodesy and remote sensing (including GPS coordinates). Your choice of ellipsoid might be different depending on your specific needs.