import os
import argparse
import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt


def get_files_from_directory(directory_path):
    file_list = os.listdir(directory_path)
    file_list.sort()
    return file_list


def load_image(file_path):
    with open(file_path, 'rb') as f:
        img = np.load(f).astype(np.float32)
    return img


def initialize_plot(image, fig_size=(6, 6)):
    fig = plt.figure(figsize=fig_size)
    im = plt.imshow(image.astype(np.uint8), animated=True)
    return fig, im


def update_fig(i, file_list, base_dir, im):
    img = load_image(os.path.join(base_dir, file_list[i]))
    im.set_array(img)
    plt.title(file_list[i])
    return im,


def main(args):
    base_dir = args.path
    file_list = get_files_from_directory(base_dir)
    img = load_image(os.path.join(base_dir, file_list[0]))
    fig, im = initialize_plot(img)

    ani = animation.FuncAnimation(fig, update_fig, frames=len(file_list),
                                  fargs=(file_list, base_dir, im),
                                  interval=500, blit=True)

    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Numpy Animation')
    parser.add_argument('path', type=str, help='Path to the input directory')
    args = parser.parse_args()
    main(args)