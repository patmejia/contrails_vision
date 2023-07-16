import numpy as np
from PIL import Image
import os
import argparse

def normalize_and_save_image(image, filename):
    image = ((image - image.min()) * (1/(image.max() - image.min()) * 255)).astype('uint8')
    image_pil = Image.fromarray(image)
    image_pil.save(filename)
    print(f'Saved {filename} successfully.')

def save_average_image(data, output_path):
    average_image = np.mean(data, axis=0)
    filename = os.path.join(output_path, 'average_image.png')
    normalize_and_save_image(average_image, filename)

def save_sum_image(data, output_path):
    summed_image = np.sum(data, axis=0)
    filename = os.path.join(output_path, 'summed_image.png')
    normalize_and_save_image(summed_image, filename)

def save_max_image(data, output_path):
    max_image = np.max(data, axis=0)
    filename = os.path.join(output_path, 'max_image.png')
    normalize_and_save_image(max_image, filename)

def save_concatenated_image(data, output_path):
    concatenated_image = np.concatenate(data, axis=1)
    filename = os.path.join(output_path, 'concatenated_image.png')
    normalize_and_save_image(concatenated_image, filename)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', help='Path to the input .npy file.')
    parser.add_argument('output_path', help='Path to the output directory.')
    args = parser.parse_args()

    # Check if paths are provided
    if not args.input_path or not args.output_path:
        raise ValueError('Input path or output path is missing.')

    # Check if the input file exists
    if not os.path.exists(args.input_path):
        raise FileNotFoundError(f"No such file or directory: '{args.input_path}'")

    # Load the .npy file
    data = np.load(args.input_path)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_path, exist_ok=True)

    # Save different versions of the image
    save_average_image(data, args.output_path)
    save_sum_image(data, args.output_path)
    save_max_image(data, args.output_path)
    save_concatenated_image(data, args.output_path)

if __name__ == "__main__":
    main()
