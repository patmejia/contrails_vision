# Roadmap
```
I. Data Preparation and Exploration
    1. Connect to the dataset and download necessary data
        - Ensure that you have access to the dataset
        - Download all necessary data and organize it in a logical manner
    2. Explore the data using visualization functions
        - Use visualization techniques to explore the data and look for patterns or trends
        - Generate summary statistics or plots to better understand the distribution of the data

II. Data Preprocessing
    1. Normalize or scale the data
        - Normalize or scale the data to ensure that all features are on the same scale
    2. Handle missing values
        - Identify and handle any missing values in the data

III. Model Selection and Training
    1. Research and select appropriate models
        - Research different models and techniques that are appropriate for the task
        - Select the model(s) that best fit your needs
    2. Train selected model(s) on preprocessed data
        - Train your selected model(s) on the preprocessed data
        - Monitor training progress and make any necessary adjustments

IV. Model Evaluation and Deployment
    1. Evaluate model performance using appropriate metrics
        - Evaluate the performance of your model(s) using appropriate evaluation metrics
        - Compare results to a baseline or benchmark to assess performance
    2. Make necessary adjustments
        - Make any necessary adjustments to your model(s) based on the evaluation results
    3. Deploy final model and make predictions on new data
        - Deploy your final model and use it to make predictions on new data
```


# To-do's:

### □: posted <br> ☑︎: completed <br> ☒: abandoned <br> ○: in progress <br> ●: on hold <br> ◌: unconfirmed

---
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

##### ○ Revise script to better modularize data transformation and visualization steps, enhancing reusability and integration with rest of the project.

##### ○ U-Net Notebook - Develop `U-Net` notebook

##### □ Notebook Tests - Create tests for `U-Net` notebook

##### ◌ Draw: script to imagine a global reference ellipsoid as a large ellipsoid that approximates the shape of the Earth on a global scale. On top of this global reference ellipsoid, there are smaller regional reference ellipsoids that provide a better fit to the local geoid in specific regions.

##### ◌ Draw: wrap data along z on globe, pass data to already existing `plot_3d` function and wrap function.