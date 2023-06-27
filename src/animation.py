import os
import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt

# Set the directory where the .npy files are stored
# BASE_DIR = './samples/sample_mini/contrails'
BASE_DIR = './samples/sample_mini/contrails'

# Get a list of all .npy files in the directory
file_list = os.listdir(BASE_DIR)
file_list.sort()  # if you want the files in alphabetical order

# Load the first image to create the base of the animation
with open(os.path.join(BASE_DIR, file_list[0]), 'rb') as f:
    img = np.load(f)

# Create a figure for the animation
fig = plt.figure(figsize=(6, 6))

# Display the first image
im = plt.imshow(img.astype(np.uint8), animated=True)

# Function to update figure
def updatefig(i):
    with open(os.path.join(BASE_DIR, file_list[i]), 'rb') as f:
        img = np.load(f).astype(np.float32)
    im.set_array(img)
    plt.title(file_list[i])
    return im,

# Create the animation
ani = animation.FuncAnimation(fig, updatefig, frames=len(file_list), interval=500, blit=True)

# Show the animation
plt.show()


# argparser is used to parse command line arguments for example to specify the path to the data directory

# import argparse

# def create_data_input_path():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--data_dir', type=str, default='data',
#                         help='Path to the data directory containing the .npy files')
#     args = parser.parse_args()
#     return args.data_dir
