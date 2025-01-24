#This code generate the images of ES and ED frame
import cv2
import pandas as pd
import os

# Load the data from CSV, assuming the first row is headers
volume_tracings = pd.read_csv('/home/trin4156/Downloads/VolumeTracings.csv')

# Make sure the 'Frame' column is numeric and rounded to nearest integer if it's a float
volume_tracings['Frame'] = pd.to_numeric(volume_tracings['Frame'], errors='coerce').round().astype('int')

# Process each video file
video_folder = '/home/trin4156/Downloads/Videos'
output_folder_images = '/home/trin4156/Desktop/codes/echonetpreprocess/images'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder_images):
    os.makedirs(output_folder_images)
print("Number of unique filenames:", volume_tracings['FileName'].nunique())
import sys
sys.exit()
# Iterate through each unique video file in the CSV
for filename in volume_tracings['FileName'].unique():
    video_path = os.path.join(video_folder, filename )
    if os.path.exists(video_path):
        # Read video
        cap = cv2.VideoCapture(video_path)

        # Get frames for ED and ES
        df_specific = volume_tracings[volume_tracings['FileName'] == filename]
        frame_numbers = sorted(df_specific['Frame'].dropna().unique())
        if len(frame_numbers) >= 2:
            ed_frame, es_frame = int(frame_numbers[-1]), int(frame_numbers[0])  # Last is ED, first is ES

            # Extract and save ED frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, ed_frame)
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(os.path.join(output_folder_images, f"{filename[:-4]}_ED.png"), frame)

            # Extract and save ES frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, es_frame)
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(os.path.join(output_folder_images, f"{filename[:-4]}_ES.png"), frame)

        # Release the video capture object
        cap.release()
    else:
        print(f"Video file {filename}.avi not found in {video_folder}.")

print("Image extraction completed.")
