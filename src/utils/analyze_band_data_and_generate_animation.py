import os
import sys
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib import animation
import matplotlib.pyplot as plt
from sklearn.metrics import jaccard_score

# CONSTANTS
_N_TIMES_BEFORE = 4
_BOUNDS = {'band_11': (243, 303), 'band_14': (-4, 2), 'band_15': (-4, 5)}
_BANDS = ['band_11', 'band_14', 'band_15', 'human_pixel_masks', 'human_individual_masks']

def load_band(base_dir, record_id, band):
    band_path = os.path.join(base_dir, record_id, f'{band}.npy')
    with open(band_path, 'rb') as f:
        band_data = np.load(f)
    return band_data

def normalize_band(band_data, bounds):
    return (band_data - bounds[0]) / (bounds[1] - bounds[0])


def display_image(img, mask, individual_masks, record_id, output_folder, dataset_type):    
    plt.figure(figsize=(18, 6))

    ax = plt.subplot(1, 3, 1)
    ax.imshow(img)
    ax.set_title('Band Image')

    ax = plt.subplot(1, 3, 2)
    ax.imshow(mask, interpolation='none')
    ax.set_title('Mask')

    ax = plt.subplot(1, 3, 3)
    ax.imshow(img)
    ax.imshow(mask, cmap='Reds', alpha=.4, interpolation='none')
    ax.set_title('Image with Mask Overlay')
    plt.savefig(os.path.join(output_folder, f'{dataset_type}_{record_id}_image_with_mask_overlay.png'))
    plt.close()
    
    n = individual_masks.shape[-1]
    plt.figure(figsize=(16, 4))
    for i in range(n):
        plt.subplot(1, n, i+1)
        plt.imshow(individual_masks[..., i], interpolation='none')
        plt.title(f'Individual Mask {i+1}')
        
    plt.savefig(os.path.join(output_folder, f'{dataset_type}_{record_id}_individual_masks.png'))
    plt.close()
    
def animate_image(img):
    fig = plt.figure(figsize=(6, 6))
    ax = plt.gca()
    im = ax.imshow(img[..., 0])
    
    ax.set_title('False Color Band Animation Over Time')
    ax.set_xlabel('Spacial dim: X Coordinate')
    ax.set_ylabel('Spacial dim: Y Coordinate')

    def draw(i):
        im.set_array(img[..., i])
        return [im]

    anim = animation.FuncAnimation(
        fig, draw, frames=img.shape[-1], interval=500, blit=True
    )

    plt.close(fig)
    return anim

def main(base_dir, record_id, output_folder, dataset_type):
    band_data = {band: load_band(base_dir, record_id, band) for band in _BANDS}

    r = normalize_band(band_data['band_15'] - band_data['band_14'], _BOUNDS['band_14'])
    g = normalize_band(band_data['band_14'] - band_data['band_11'], _BOUNDS['band_15'])
    b = normalize_band(band_data['band_14'], _BOUNDS['band_11'])

    false_color = np.clip(np.stack([r,g,b], axis=2), 0 ,1)
    img = false_color[..., _N_TIMES_BEFORE]

    display_image(img, band_data['human_pixel_masks'], band_data['human_individual_masks'], record_id, output_folder, dataset_type)
    animation = animate_image(false_color)

    video_path = os.path.join(output_folder, f"{dataset_type}_{record_id}_animation.mp4")
    animation.save(video_path)
    plt.show()

if __name__ == '__main__':
    base_directory = './'
    output_directory = os.path.join(base_directory, 'output')
    script_name = 'analyze_band_data_and_generate_animation'
    output_subdirectory = os.path.join(output_directory, script_name)
    os.makedirs(output_subdirectory, exist_ok=True)

    record_id = sys.argv[1]
    dataset_type = sys.argv[2]  # Pass 'train' or 'validation' as a command-line argument

    base_dir = os.path.join(base_directory, f'samples/kaggle_competition_mini_sample/{dataset_type}')
    main(base_dir, record_id, output_subdirectory, dataset_type)
