import os
import argparse
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

_T11_BOUNDS = (243, 303)
_CLOUD_TOP_TDIFF_BOUNDS = (-4, 5)
_TDIFF_BOUNDS = (-4, 2)

def main():
    args = parse_args()

    record_ids = select_all_records(args)

    for record_id in np.random.choice(record_ids, args.n_records, replace=False):
        visualize_contrails(args, record_id)

def parse_args():
    parser = argparse.ArgumentParser(description='Run contrails visualization for random records')
    parser.add_argument('--base_dir', type=str, required=True, help='Base directory for the data')
    parser.add_argument('--n_records', type=int, default=5, help='Number of records to display')
    parser.add_argument('--n_times_before', type=int, default=4, help='Number of images before the labeled frame')
    return parser.parse_args()

def select_all_records(args):
    contrails_dir = os.path.join(args.base_dir, 'contrails')
    record_ids = [f[:-4] for f in os.listdir(contrails_dir) if f.endswith('.npy')]  # Extract record IDs from .npy files
    print(f'Found {len(record_ids)} records')
    return record_ids

def visualize_contrails(args, record_id):
    print(f'Displaying record_id: {record_id}')

    data = load_data(args.base_dir, record_id)
    false_color = preprocess_data(data)

    visualize_data(false_color, args.n_times_before, data['human_pixel_mask'], data['human_individual_mask'])
    animate_data(false_color)

def load_data(base_dir, record_id):
    with open(os.path.join(base_dir, 'contrails', record_id + '.npy'), 'rb') as f:
        data = np.load(f, allow_pickle=True).item()
    print(f"Data shape: {data.shape}, data dtype: {data.dtype}")
    print(f"Data keys: {data.keys()}, data values: {data.values()}")
    return data

def preprocess_data(data):
    r = normalize_range(data[..., 3] - data[..., 2], _TDIFF_BOUNDS)
    g = normalize_range(data[..., 2] - data[..., 1], _CLOUD_TOP_TDIFF_BOUNDS)
    b = normalize_range(data[..., 2], _T11_BOUNDS)
    return np.clip(np.stack([r, g, b], axis=2), 0, 1)

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
    plt.figure(figsize=(16, 4))
    for i in range(n):
        plt.subplot(1, n, i+1)
        plt.imshow(human_individual_mask[..., i], interpolation='none')
    plt.show()

def animate_data(false_color):
    fig = plt.figure(figsize=(6, 6))
    im = plt.imshow(false_color[..., 0])

    def draw(i):
        im.set_array(false_color[..., i])
        return [im]

    anim = animation.FuncAnimation(fig, draw, frames=false_color.shape[-1], interval=500, blit=True)
    plt.show()

if __name__ == '__main__':
    main()
