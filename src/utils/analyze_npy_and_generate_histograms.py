import os
import numpy as np
import matplotlib.pyplot as plt

def analyze_data(input_directory, output_directory):
    # Loop over each record directory
    for record_dir in os.listdir(input_directory):
        record_path = os.path.join(input_directory, record_dir)

        if os.path.isdir(record_path):
            band_data = []
            band_names = []
            
            # Loop over each band file in the record directory
            for file in os.listdir(record_path):
                if file.endswith(".npy"):
                    filepath = os.path.join(record_path, file)
                    data = np.load(filepath)

                    band_data.append(data.flatten())
                    band_names.append(file.replace('.npy', ''))
            
            # Plot overlayed histogram for all bands
            plt.figure(figsize=(10, 7))
            for data, name in zip(band_data, band_names):
                plt.hist(data, bins=50, alpha=0.5, label=name)
            
            plt.title(f'Overlayed Histogram of Pixel Intensities for Record {record_dir}')
            plt.xlabel('Pixel Intensity')
            plt.ylabel('Frequency')
            plt.legend(loc='upper right')
            
            # Save the histogram as .png file
            hist_filename = f"{record_dir}_overlayed_hist.png"
            hist_filepath = os.path.join(output_directory, hist_filename)
            plt.savefig(hist_filepath)
            plt.close()

# Specify the base directory of your project
base_directory = './'

# Specify input directories
input_directory_train = os.path.join(base_directory, 'samples/kaggle_competition_mini_sample/train')
input_directory_test = os.path.join(base_directory, 'samples/kaggle_competition_mini_sample/test')
input_directory_validation = os.path.join(base_directory, 'samples/kaggle_competition_mini_sample/validation')

# Specify output directory
output_directory = os.path.join(base_directory, 'output')

# Create a new directory inside 'output' named after the script
output_subdirectory = os.path.join(output_directory, 'analyze_npy_and_generate_histograms')
os.makedirs(output_subdirectory, exist_ok=True)

# Analyze data in the 'train' and 'test' directories
analyze_data(input_directory_train, output_subdirectory)
analyze_data(input_directory_test, output_subdirectory)
analyze_data(input_directory_validation, output_subdirectory)