import cv2
import json
import numpy as np

# Path to the video file
video_path = 'testinput.mp4'

# Open the video file
cap = cv2.VideoCapture(video_path)

# Initialize an empty list to store the flattened frames
frames_data = []

# Loop through the video frames
while True:
    # Read the next frame
    success, frame = cap.read()
    if not success:
        break

    # Resize frame to 64x64 and convert to grayscale
    frame = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (5, 1))

    # Normalize pixel values to range [0, 1]
    frame = frame.astype(np.float32) / 255.0

    # Flatten the frame array
    frame_flattened = frame.flatten()

    # Append the flattened frame to the list
    frames_data.append(frame_flattened.tolist())

# Release the video capture object
cap.release()

# Write the frames data to a JSON file
with open('frames_data.json', 'w') as json_file:
    json.dump(frames_data, json_file)
