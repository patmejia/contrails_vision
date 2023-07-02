import os
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import multiprocessing as mp


def parse_args():
    parser = argparse.ArgumentParser(description='Run contrails visualization for random records')
    parser.add_argument('--base_dir', type=str, required=True, help='Base directory for the data')
    parser.add_argument('--n_records', type=int, default=5, help='Number of records to display')
    parser.add_argument('--n_times_before', type=int, default=4, help='Number of images before the labeled frame')
    return parser.parse_args()


def get_record_path(base_dir, record_id):
    return os.path.join(base_dir, f'{record_id}.npy')


def select_all_records(args):
    record_ids = [f[:-4] for f in os.listdir(args.base_dir) if f.endswith('.npy')]
    print(f'Found {len(record_ids)} records')
    return record_ids


def load_data(base_dir, record_id):
    with open(get_record_path(base_dir, record_id), 'rb') as f:
        data = np.load(f, allow_pickle=True)
        print(f'Loaded record_id: {record_id}')
    return data


def normalize_range(data, bounds):
    return (data - bounds[0]) / (bounds[1] - bounds[0])


def preprocess_data(data):
    t11_bounds = (243, 303)
    cloud_top_tdiff_bounds = (-4, 5)
    tdiff_bounds = (-4, 2)

    r = normalize_range(data[..., 3] - data[..., 2], tdiff_bounds)
    g = normalize_range(data[..., 2] - data[..., 1], cloud_top_tdiff_bounds)
    b = normalize_range(data[..., 2], t11_bounds)

    result = np.clip(np.stack([r, g, b], axis=2), 0, 1)
    result = (result * 255).astype(np.uint8)

    return result


def visualize_data(false_color, n_times_before, human_pixel_mask, human_individual_mask):
    img = false_color[..., min(n_times_before, false_color.shape[2] - 1)]

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


def process_record(record_id, args):
    # Load and process the data for a single record
    data = load_data(args.base_dir, record_id)
    false_color = preprocess_data(data)
    human_pixel_mask = data[..., -2].astype(np.float32)
    human_individual_mask = np.expand_dims(data[..., -1], axis=-1).astype(np.float32)

    return false_color, args.n_times_before, human_pixel_mask, human_individual_mask


def main():
    matplotlib.use('TkAgg')
    args = parse_args()

    record_ids = select_all_records(args)

    if args.n_records > len(record_ids):
        print(f"Error: Requested number of records ({args.n_records}) exceeds available records ({len(record_ids)})")
        return

    for record_id in record_ids[:args.n_records]:
        false_color, n_times_before, human_pixel_mask, human_individual_mask = process_record(record_id, args)
        visualize_data(false_color, n_times_before, human_pixel_mask, human_individual_mask)


if __name__ == '__main__':
    main()
