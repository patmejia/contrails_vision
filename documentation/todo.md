# To-do's:

### □: posted <br> ☑︎: completed <br> ☒: abandoned <br> ○: in progress <br> ●: on hold <br> ◌: unconfirmed

---

##### ◌ add :"load bands of data, normalize them, create false-color images, and generate animations over time for visual inspection" to viz script"
##### ☑︎ Resolve `run.py` and `kaggle_competition_mini_sample` Dataset Incompatibility
Shape difference information:

```
(contrail_env) ➜  contrails-vision git:(main) ✗ python src/utils/get_shape.py samples/kaggle_competition_mini_sample/test/1000834164244036115/band_08.npy 
Shape: (256, 256, 8)
Size: 524288
(contrail_env) ➜  contrails-vision git:(main) ✗ python src/utils/get_shape.py samples/false_color_mini_sample/contrails/1108741208571075.npy 
Shape: (256, 256, 4)
Size: 262144
(contrail_env) ➜  contrails-vision git:(main) ✗ 
```

##### ☑︎ Data Retrieval - Execute Python code to fetch data:
```python
BASE_DIR = '/kaggle/input/google-research-identify-contrails-reduce-global-warming/train'
N_TIMES_BEFORE = 4
record_id = '1704010292581573769'

def load_band_data(band_name):
    with open(os.path.join(BASE_DIR, record_id, f'{band_name}.npy'), 'rb') as f:
        return np.load(f)

band11 = load_band_data('band_11')
band14 = load_band_data('band_14')
band15 = load_band_data('band_15')
human_pixel_mask = load_band_data('human_pixel_masks')
human_individual_mask = load_band_data('human_individual_masks')
```
##### ☑︎ Create data roadmap for project

##### ○ Revise script to better modularize data transformation and visualization steps, enhancing reusability and integration with rest of the project.

##### ○ U-Net Notebook - Develop `U-Net` notebook

##### □ Notebook Tests - Create tests for `U-Net` notebook

##### □ Does "# Convert data to float64 to avoid potential overflows" in `compute_stats` function in `utils.py` cause any issues? If so, how to resolve? Or, what are people doing to resolve this issue? If, it is not an issue, why not? or why is it not a problem? i.e. changing data type from `uint16` to `float64`?
```
def compute_stats(data, filepath):
    try:
        # Convert data to float64 to avoid potential overflows
        data = data.astype(np.float64)
        
        stats = {
            'shape': data.shape,
            'size': data.size,
            'mean': np.mean(data),
            'std_dev': np.std(data),
            'min': np.min(data),
            'max': np.max(data),
            'all_zeros': np.all(data == 0),
            'zero_count': np.count_nonzero(data == 0),  # count of zeros
            'non_zero_count': np.count_nonzero(data)  # count of non-zeros
        }
    except Exception as e:
        print(f"Error processing file {filepath}: {e}")
        print(f"Data type: {data.dtype}, Data min: {np.min(data)}, Data max: {np.max(data)}")
        return None
    return stats
```

##### ◌ Draw: script to imagine a global reference ellipsoid as a large ellipsoid that approximates the shape of the Earth on a global scale. On top of this global reference ellipsoid, there are smaller regional reference ellipsoids that provide a better fit to the local geoid in specific regions.

##### ◌ Draw: wrap data along z on globe, pass data to already existing `plot_3d` function and wrap function.