import os
import sys
import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt

# CONSTANTS
_N_TIMES_BEFORE = 4
_T11_BOUNDS = (243, 303)
_CLOUD_TOP_TDIFF_BOUNDS = (-4, 5)
_TDIFF_BOUNDS = (-4, 2)
_BANDS = ['band_11', 'band_14', 'band_15', 'human_pixel_masks', 'human_individual_masks']

def print_debug(*args):
    print("[DEBUG]", *args)

def load_band(base_dir, record_id, band):
    print_debug(f"Loading numpy array for band: {band}")
    band_path = os.path.join(base_dir, record_id, f'{band}.npy')
    with open(band_path, 'rb') as f:
        band_data = np.load(f)
    print_debug(f"Loaded band: {band} with shape {band_data.shape}")
    return band_data

def normalize_band(band_data, bounds):
    print_debug(f"Normalizing band data with bounds: {bounds}")
    normalized_data = (band_data - bounds[0]) / (bounds[1] - bounds[0])
    print_debug(f"Normalization complete. Data min: {normalized_data.min()}, max: {normalized_data.max()}")
    return normalized_data

def display_image(img, mask, individual_masks, record_id):    
    print(individual_masks)
    print_debug("Displaying image.")
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
    plt.savefig(os.path.join(output_folder, f'{record_id}_image_with_mask_overlay.png'))

    n = individual_masks.shape[-1]
    plt.figure(figsize=(16, 4))
    for i in range(n):
        plt.subplot(1, n, i+1)
        plt.imshow(individual_masks[..., i], interpolation='none')
        plt.title(f'Individual Mask {i+1}')
        
    plt.savefig(os.path.join(output_folder, f'{record_id}_individual_masks.png'))
    
    print_debug("Image displayed.")

        
def animate_image(img):
    print_debug("Animating image.")
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
    print_debug("Animation created.")
    return anim

def main(base_dir, record_id):
    print_debug(f"Running main function with base_dir={base_dir} and record_id={record_id}")

    band11 = load_band(base_dir, record_id, 'band_11')
    band14 = load_band(base_dir, record_id, 'band_14')
    band15 = load_band(base_dir, record_id, 'band_15')
    human_pixel_mask = load_band(base_dir, record_id, 'human_pixel_masks')
    human_individual_mask = load_band(base_dir, record_id, 'human_individual_masks')

    r = normalize_band(band15 - band14, _TDIFF_BOUNDS)
    g = normalize_band(band14 - band11, _CLOUD_TOP_TDIFF_BOUNDS)
    b = normalize_band(band14, _T11_BOUNDS)

    false_color = np.clip(np.stack([r,g,b], axis=2), 0 ,1)

    img = false_color[..., _N_TIMES_BEFORE]

    display_image(img, human_pixel_mask, human_individual_mask, record_id)
    return animate_image(false_color)


if __name__ == '__main__':
    # Create the output folder if it doesn't exist
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Set the base directory and record ID
    base_dir = "samples/kaggle_competition_mini_sample/train"
    record_id = sys.argv[1]

    # Call the main function with the base directory and record ID as arguments
    animation = main(base_dir, record_id)

    # Save the animation as a video
    video_path = os.path.join(output_folder, "animation.mp4")
    animation.save(video_path)

    # Display the animation
    plt.show()

    