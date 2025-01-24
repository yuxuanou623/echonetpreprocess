# This code generate closed masks ( masks dont have empty pixels inside) and save the output's mask pixel to be 2

import os
from skimage import io, color
from skimage.morphology import binary_closing
from skimage.filters import threshold_otsu
from skimage import img_as_ubyte  # Import to handle data type conversion
import numpy as np

# Define paths
input_folder = '/home/trin4156/Desktop/codes/echonetpreprocess/masks'
output_folder = '/home/trin4156/Desktop/codes/echonetpreprocess/closed'

# Create the output directory if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate through each image file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.png'):  # Adjust this as needed for your file type
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Load the image
        image = io.imread(input_path)

        # Convert the image to grayscale if it's not already
        if len(image.shape) == 3:
            gray_image = color.rgb2gray(image)
        else:
            gray_image = image  # Assume the image is already in grayscale

        # Convert grayscale image to binary
        try:
            thresh = threshold_otsu(gray_image)
            binary_image = gray_image > thresh
        except ValueError:
            print(f"Not enough image data for Otsu's method in {filename}. Skipping...")
            continue

        # Apply morphological closing
        closed_image = binary_closing(binary_image)

        # Convert closed mask values to 2 and background to 0
        closed_image = (closed_image > 0).astype(int) * 2

        # Convert the image to 8-bit unsigned byte format
        closed_image = img_as_ubyte(closed_image)

        # Save the processed image
        io.imsave(output_path, closed_image, check_contrast=False)  # Ignore low contrast warning

print("All masks have been processed and saved.")
