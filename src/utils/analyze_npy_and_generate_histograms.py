import os
import numpy as np
import matplotlib.pyplot as plt

def analyze_data(input_directory, output_directory):
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith(".npy"):
                filepath = os.path.join(root, file)
                data = np.load(filepath)
                
                # Compute statistics
                shape = data.shape
                size = data.size
                mean = np.mean(data)
                std_dev = np.std(data)
                min_val = np.min(data)
                max_val = np.max(data)
                all_zeros = np.all(data == 0)
                
                print(f"File: {filepath}")
                print(f"Shape: {shape}, Size: {size}")
                print(f"Mean: {mean}, Std Dev: {std_dev}, Min: {min_val}, Max: {max_val}")
                print(f"All zeros: {all_zeros}")
                print("---")
                
                # Plot histogram of pixel intensities
                plt.hist(data.flatten(), bins=50, color='c')
                plt.title('Histogram of Pixel Intensities')
                plt.xlabel('Pixel Intensity')
                plt.ylabel('Frequency')
                
                # Save the histogram as .png file
                hist_filename = f"{os.path.basename(root)}_{file.replace('.npy', '_hist.png')}"
                hist_filepath = os.path.join(output_directory, hist_filename)
                plt.savefig(hist_filepath)
                plt.close()

# Specify the base directory of your project
base_directory = './'

# Specify input directories
input_directory_train = os.path.join(base_directory, 'samples/kaggle_competition_mini_sample/train')
input_directory_test = os.path.join(base_directory, 'samples/kaggle_competition_mini_sample/test')

# Specify output directory
output_directory = os.path.join(base_directory, 'output')

# Create a new directory inside 'output' named after the script
output_subdirectory = os.path.join(output_directory, 'analyze_npy_and_generate_histograms')
os.makedirs(output_subdirectory, exist_ok=True)

# Analyze data in the 'train' and 'test' directories
analyze_data(input_directory_train, output_subdirectory)
analyze_data(input_directory_test, output_subdirectory)
