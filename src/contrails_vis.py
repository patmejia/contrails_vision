# Dependencies
import os
import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt
from IPython import display

# Constants
BASE_DIR = '/kaggle/input/google-research-identify-contrails-reduce-global-warming/train'
N_TIMES_BEFORE = 4
record_id = '1704010292581573769'

# Function to load numpy arrays
def load_data(record_id, band_id):
    with open(os.path.join(BASE_DIR, record_id, band_id), 'rb') as f:
        data = np.load(f)
    return data

# Function to normalize data range
def normalize_range(data, bounds):
    """Maps data to the range [0, 1]."""
    return (data - bounds[0]) / (bounds[1] - bounds[0])

# Function to create a false color image
def create_false_color_image(band15, band14, band11, _TDIFF_BOUNDS, _CLOUD_TOP_TDIFF_BOUNDS, _T11_BOUNDS):
    r = normalize_range(band15 - band14, _TDIFF_BOUNDS)
    g = normalize_range(band14 - band11, _CLOUD_TOP_TDIFF_BOUNDS)
    b = normalize_range(band14, _T11_BOUNDS)
    false_color = np.clip(np.stack([r, g, b], axis=2), 0, 1)
    return false_color

# Function to display data
def display_data(false_color, human_pixel_mask, human_individual_mask):
    img = false_color[..., N_TIMES_BEFORE]
    plt.figure(figsize=(18, 6))
    ax = plt.subplot(1, 3, 1)
    ax.imshow(img)
    ax.set_title('False color image')

    ax = plt.subplot(1, 3, 2)
    ax.imshow(human_pixel_mask, interpolation='none')
    ax.set_title('Ground truth contrail mask')

    ax = plt.subplot(1, 3, 3)
    ax.imshow(img)
    ax.imshow(human_pixel_mask, cmap='Reds', alpha=.4, interpolation='none')
    ax.set_title('Contrail mask on false color image');

# Function to display individual human masks
def display_individual_masks(human_individual_mask):
    n = human_individual_mask.shape[-1]
    plt.figure(figsize=(16, 4))
    for i in range(n):
        plt.subplot(1, n, i+1)
        plt.imshow(human_individual_mask[..., i], interpolation='none')

# Function to create animation
def animate_false_color(false_color):
    fig = plt.figure(figsize=(6, 6))
    im = plt.imshow(false_color[..., 0])
    def draw(i):
        im.set_array(false_color[..., i])
        return [im]
    anim = animation.FuncAnimation(
        fig, draw, frames=false_color.shape[-1], interval=500, blit=True
    )
    plt.close()
    display.HTML(anim.to_jshtml())

# Execution
band11 = load_data(record_id, 'band_11.npy')
band14 = load_data(record_id, 'band_14.npy')
band15 = load_data(record_id, 'band_15.npy')
human_pixel_mask = load_data(record_id, 'human_pixel_masks.npy')
human_individual_mask = load_data(record_id, 'human_individual_masks.npy')

_T11_BOUNDS = (243, 303)
_CLOUD_TOP_TDIFF_BOUNDS = (-4, 5)
_TDIFF_BOUNDS = (-4, 2)

false_color = create_false_color_image(band15, band14, band11, _TDIFF_BOUNDS, _CLOUD_TOP_TDIFF_BOUNDS, _T11_BOUNDS)
display_data(false_color, human_pixel_mask, human_individual_mask)
display_individual_masks(human_individual_mask)
animate_false_color(false_color)
