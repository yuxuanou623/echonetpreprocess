# This code generate the image with overlayed masks and also vertex
import cv2
import pandas as pd
import numpy as np
import os

# Load the data from CSV, assuming the first row is headers
volume_tracings = pd.read_csv('/home/trin4156/Downloads/VolumeTracings.csv')

# Define the video folder and output folder
video_folder = '/home/trin4156/Downloads/Videos'
output_folder_masks = '/home/trin4156/Desktop/codes/echonetpreprocess/thickness2'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder_masks):
    os.makedirs(output_folder_masks)

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

                    # Create an overlay to draw the polygon and vertices on
                    overlay = frame.copy()
                    cv2.polylines(overlay, [polygon], isClosed=True, color=(0, 255, 0), thickness=2)

                    # Draw vertices as yellow circles
                    for point in points:
                        cv2.circle(overlay, point, radius=1, color=(0, 255, 255), thickness=-1)  # -1 fills the circle

                    # Blend the overlay with the original frame
                    alpha = 0.4  # Transparency factor.
                    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

                    # Save the frame with the overlay to the output folder
                    output_path = os.path.join(output_folder_masks, f"{filename}_{frame_type}.png")
                    cv2.imwrite(output_path, frame)

        # Release the video capture object
        cap.release()

print("All videos processed and frames saved.")
