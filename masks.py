# this code generate the masks of pixel value 255 and also generate the visualization of the mask overlaying the original frame
import cv2
import pandas as pd
import numpy as np
import os

# Load the data from CSV, assuming the first row is headers
volume_tracings = pd.read_csv('/home/trin4156/Downloads/VolumeTracings.csv')

# Define the video folder and output folder for videos and polygons
video_folder = '/home/trin4156/Downloads/Videos'
output_folder_masks = '/home/trin4156/Desktop/codes/echonetpreprocess/overlay'
output_folder_polygons = '/home/trin4156/Desktop/codes/echonetpreprocess/masks'  # New folder for polygons

# Create the output folders if they don't exist
if not os.path.exists(output_folder_masks):
    os.makedirs(output_folder_masks)
if not os.path.exists(output_folder_polygons):
    os.makedirs(output_folder_polygons)

# Iterate through each unique video file in the CSV
for filename in volume_tracings['FileName'].unique():
    video_path = os.path.join(video_folder, filename)
    if os.path.exists(video_path):
        # Read video
        cap = cv2.VideoCapture(video_path)

        # Get frames for ED and ES
        df_specific = volume_tracings[volume_tracings['FileName'] == filename]
        frame_numbers = sorted(df_specific['Frame'].dropna().unique())
        if len(frame_numbers) >= 2:
            for frame_type, frame_number in zip(['ED', 'ES'], [frame_numbers[-1], frame_numbers[0]]):
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                ret, frame = cap.read()
                if ret:
                    # Extract polygon vertices
                    rows = df_specific[df_specific['Frame'] == frame_number]
                    points = []
                    for _, row in rows.iterrows():
                        for i in range(1, 3):  # Assuming X1, X2, Y1, Y2 columns
                            points.append((int(row[f'X{i}']), int(row[f'Y{i}'])))

                    # Convert points list to a numpy array and reshape for drawing
                    polygon = np.array(points, dtype=np.int32).reshape((-1, 1, 2))

                    # Create an overlay to draw the polygon on
                    overlay = np.zeros_like(frame)
                    cv2.polylines(overlay, [polygon], isClosed=True, color=(255, 255, 255), thickness=2)

                    # Save the polygon image
                    polygon_path = os.path.join(output_folder_polygons, f"{filename[:-4]}_{frame_type}.png")
                    cv2.imwrite(polygon_path, overlay)

                    # Blend the overlay with the original frame and save
                    alpha = 0.4  # Transparency factor.
                    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
                    output_path = os.path.join(output_folder_masks, f"{filename[:-4]}_{frame_type}.png")
                    cv2.imwrite(output_path, frame)

        # Release the video capture object
        cap.release()

print("All videos processed and frames saved.")
