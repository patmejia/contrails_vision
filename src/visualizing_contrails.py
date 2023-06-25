import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

parser = argparse.ArgumentParser(description='Visualizing Contrails')
parser.add_argument('--base_dir', type=str, required=True, help='Base directory for the data')
parser.add_argument('--n_times_before', type=int, default=4, help='Number of images before the labeled frame')
parser.add_argument('--record_id', type=str, required=True, help='Record ID')

args = parser.parse_args()

BASE_DIR = args.base_dir
N_TIMES_BEFORE = args.n_times_before
record_id = args.record_id

# load numpy array
with open(os.path.join(BASE_DIR, 'contrails', record_id + '.npy'), 'rb') as f:
    data = np.load(f)
print(f"Data shape: {data.shape}, data dtype: {data.dtype}")
print(f"Data keys: {data.keys()}, data values: {data.values()}")

# Extract data
band11 = data['band11']
band14 = data['band14']
band15 = data['band15']
human_pixel_mask = data['human_pixel_mask']
human_individual_mask = data['human_individual_mask']



_T11_BOUNDS = (243, 303)
_CLOUD_TOP_TDIFF_BOUNDS = (-4, 5)
_TDIFF_BOUNDS = (-4, 2)

def normalize_range(data, bounds):
    """Maps data to the range [0, 1]."""
    return (data - bounds[0]) / (bounds[1] - bounds[0])

r = normalize_range(band15 - band14, _TDIFF_BOUNDS)
g = normalize_range(band14 - band11, _CLOUD_TOP_TDIFF_BOUNDS)
b = normalize_range(band14, _T11_BOUNDS)
false_color = np.clip(np.stack([r, g, b], axis=2), 0, 1)

# Visualize data
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
ax.set_title('Contrail mask on false color image')
plt.show()

# Individual human masks
n = human_individual_mask.shape[-1]
plt.figure(figsize=(16, 4))
for i in range(n):
    plt.subplot(1, n, i+1)
    plt.imshow(human_individual_mask[..., i], interpolation='none')
plt.show()

# Animation
fig = plt.figure(figsize=(6, 6))
im = plt.imshow(false_color[..., 0])
def draw(i):
    im.set_array(false_color[..., i])
    return [im]
anim = animation.FuncAnimation(
    fig, draw, frames=false_color.shape[-1], interval=500, blit=True
)
plt.show()
