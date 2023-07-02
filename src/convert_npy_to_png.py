import numpy as np
from PIL import Image

# Load the .npy file
data = np.load('path/to/your/file.npy')

# Iterate through the images and save them as JPEG or PNG
for i, image in enumerate(data):
    # Convert the image to PIL format
    image_pil = Image.fromarray(image)

    # Define the desired filename (e.g., image_001.jpg, image_002.jpg, ...)
    filename = f'image_{i+1:03d}.jpg'  # Adjust the format based on your preference (jpg or png)

    # Save the image as JPEG or PNG
    image_pil.save(filename)

    print(f'Saved {filename} successfully.')
