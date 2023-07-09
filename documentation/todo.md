## Notes: 

#### ➲ Other run options

```bash
python src/main.py
python run.py samples/kaggle_competition_mini_sample/test/1000834164244036115 output
python src/utils//visualize.py --base_dir samples/sample_mini/contrails --n_records 2 --n_times_before 4
python src/utils/get_shape.py samples/sample_mini/contrails/1108741208571075.npy
python src/utils/coordinate_converter.py samples/kaggle_competition_mini_sample/test/1000834164244036115 output
python src/utils/get_shape.py samples/kaggle_competition_sample/test/1000834164244036115/band_08.npy
python src/utils/rle_encoding_submission.py samples/kaggle_competition_mini_sample 1
```
# Roadmap
 ### □: posted <br> ☑︎: completed <br> ☒: abandoned <br> ○: in progress <br> ●: on hold <br> ◌: unconfirmed
---
##### □ Revise script to better modularize data transformation and visualization steps, enhancing reusability and integration with rest of the project.
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
#### □ Draw: scriprt to imagine a global reference ellipsoid as a large ellipsoid that approximates the shape of the Earth on a global scale. On top of this global reference ellipsoid, there are smaller regional reference ellipsoids that provide a better fit to the local geoid in specific regions.

