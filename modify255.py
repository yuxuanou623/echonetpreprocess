# This code change the mask pixel value from 2 to 255 in order to visualize the masks

import os
from skimage import io
import numpy as np

# Define the path to the closed folder
input_folder = '/home/trin4156/Desktop/codes/echonetpreprocess/closed'
output_folder = '/home/trin4156/Desktop/codes/echonetpreprocess/modified'

# Create the output directory if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate through each image file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.png'):  # Adjust as needed for your file type
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # Load the image
        image = io.imread(input_path)

        # Modify pixel values: 2 to 255
        modified_image = np.where(image == 2, 255, image)

        # Save the modified image
        io.imsave(output_path, modified_image)

        # Verify that all pixels are either 0 or 255
        unique_values = np.unique(modified_image)
        if not np.all(np.isin(unique_values, [0, 255])):
            print(f"{filename}: Contains unexpected pixel values.")


print("All images have been processed and saved.")
