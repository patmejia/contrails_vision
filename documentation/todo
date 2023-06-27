# Roadmap
 ### □: posted <br> ☑︎: completed <br> ☒: abandoned <br> ○: in progress <br> ●: on hold <br> ◌: not started
---
##### □ U-Net Notebook - Develop `U-Net` notebook

##### □ Notebook Tests - Create tests for `U-Net` notebook

##### □ Data Retrieval - Execute Python code to fetch data:

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
