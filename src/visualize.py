import os
import argparse
import subprocess
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FFMpegWriter


_T11_BOUNDS = (243, 303)
_CLOUD_TOP_TDIFF_BOUNDS = (-4, 5)
_TDIFF_BOUNDS = (-4, 2)

def parse_args():
    parser = argparse.ArgumentParser(description='Run contrails visualization for random records')
    parser.add_argument('--base_dir', type=str, required=True, help='Base directory for the data')
    parser.add_argument('--n_records', type=int, default=5, help='Number of records to display')
    parser.add_argument('--n_times_before', type=int, default=4, help='Number of images before the labeled frame')
    return parser.parse_args()

def get_record_path(base_dir, record_id):
    return os.path.join(base_dir, f'{record_id}.npy')

def select_all_records(args):
    record_ids = [f[:-4] for f in os.listdir(args.base_dir) if f.endswith('.npy')]  # Extract record IDs from .npy files
    print(f'Found {len(record_ids)} records')
    return record_ids


def load_data(base_dir, record_id):
    with open(get_record_path(base_dir, record_id), 'rb') as f:
        data = np.load(f, allow_pickle=True)
        print(f'Loaded record_id: {record_id}')
    return data


def preprocess_data(data):
    r = normalize_range(data[..., 3] - data[..., 2], _TDIFF_BOUNDS)
    g = normalize_range(data[..., 2] - data[..., 1], _CLOUD_TOP_TDIFF_BOUNDS)
    b = normalize_range(data[..., 2], _T11_BOUNDS)

    result = np.clip(np.stack([r, g, b], axis=2), 0, 1)
    result = (result * 255).astype(np.uint8)  # Convert to uint8 and range 0-255

    return result

def normalize_range(data, bounds):
    return (data - bounds[0]) / (bounds[1] - bounds[0])

def visualize_data(false_color, n_times_before, human_pixel_mask, human_individual_mask):
    img = false_color[..., min(n_times_before, false_color.shape[2]-1)]

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
    ax.set_title('Contrail mask on false color image')
    plt.show()

    n = human_individual_mask.shape[-1]
    print(f'Found {n} contrails')
    print(f'human_individual_mask.shape: {human_individual_mask.shape}')
    print(f'False color image shape: {img.shape}, dtype: {img.dtype}')
    print(f'Ground truth contrail mask shape: {human_pixel_mask.shape}, dtype: {human_pixel_mask.dtype}')
    
    # Convert 1D mask to 2D mask
    human_individual_mask_2d = np.expand_dims(human_individual_mask, axis=-1)
    human_individual_mask_2d = np.squeeze(human_individual_mask_2d, axis=-1)
    human_individual_mask_2d = human_individual_mask_2d[..., np.newaxis]  # Add new axis
    human_individual_mask_2d = np.squeeze(human_individual_mask_2d, axis=-1)  # Remove extra dimension
    
    n = human_individual_mask_2d.shape[-1]
    for i in range(n):
        plt.subplot(1, n, i+1)
        human_individual_mask_2d_reshaped = np.squeeze(np.expand_dims(human_individual_mask_2d[..., i], axis=-1))
        print(f'human_individual_mask.shape before imshow: {human_individual_mask_2d_reshaped.shape}')
        plt.imshow(human_individual_mask_2d_reshaped, interpolation='none', cmap='gray')  
    plt.show()


def animate_data(false_color):
    fig = plt.figure(figsize=(6, 6))
    im = plt.imshow(false_color[..., 0])

    def draw(i):
        im.set_array(false_color[..., i])
        return [im]

    anim = animation.FuncAnimation(fig, draw, frames=false_color.shape[-1], interval=500, blit=True)
    writer = FFMpegWriter(fps=1)
    with writer.saving(fig, "animation.mp4", dpi=100):
        for i in range(false_color.shape[-1]):
            im.set_array(false_color[..., i])
            writer.grab_frame()


def visualize_contrails(args, record_id):
    print(f'Displaying record_id: {record_id}')

    data = load_data(args.base_dir, record_id)
    false_color = preprocess_data(data)
    processed_data = np.concatenate([data[..., None], false_color[..., None]], axis=2)  # add new axis to data
    print(f'Processed data shape: {processed_data.shape}')
    human_pixel_mask = data[..., -2].astype(np.float32)
    human_individual_mask = data[..., -1].astype(np.float32)

    print(np.any(np.isnan(processed_data)))
    print(np.any(np.isinf(processed_data)))

    visualize_data(false_color, args.n_times_before, human_pixel_mask, human_individual_mask)
    # animate_data(false_color)


def main():
    matplotlib.use('TkAgg')
    args = parse_args()

    record_ids = select_all_records(args)

    for record_id in np.random.choice(record_ids, args.n_records, replace=False):
        visualize_contrails(args, record_id)

if __name__ == '__main__':
    main()
