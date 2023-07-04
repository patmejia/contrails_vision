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

### other link: 

#### [STAC](https://stacspec.org/en/tutorials/1-read-stac-python/)