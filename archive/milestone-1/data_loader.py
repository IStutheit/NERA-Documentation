import cv2
import json
import numpy as np
import requests
import os


def process_video(video_path):
    frames = []
    cap = cv2.VideoCapture(video_path)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Resize the frame
        resized_frame = cv2.resize(frame, (25, 25))
        
        # Convert to grayscale
        gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
        
        # Flatten the frame
        flattened_frame = gray_frame.flatten()
        
        # Append the flattened frame to the list
        frames.append(flattened_frame.tolist())
    
    cap.release()

    frames.pop()

    for i in range(len(frames)):
        for j in range(len(frames[i])):
            frames[i][j] = frames[i][j]/255
    
    return frames

def process_labels(file_path):
    labels = []
    with open(file_path, 'r') as file:
        content = file.read()
        
    json_objects = content.split('\n')

    for json_str in json_objects:
        if json_str.strip():  # Skip empty lines
            label = [0 for i in range(22)]
            data = json.loads(json_str)
            key_presses = data.get('keyboard', None).get('keys', None)
            mouse_presses = data.get('mouse', None).get('buttons',None)
            if json_objects.index(json_str) != 0:
                data_prev = json.loads(json_objects[json_objects.index(json_str) - 1])
                yaw_change = data.get('yaw', None) - data_prev.get('yaw', None)
                pitch_change = data.get('pitch', None) - data_prev.get('pitch', None)
            else:
                yaw_change = 0
                pitch_change = 0

            if 0 in mouse_presses:
                label[0] = 1
                
            if "key.keyboard.s" in key_presses:
                label[1] = 1
                
            label[2] = yaw_change
            label[3] = pitch_change

            if "key.keyboard.q" in key_presses:
                label[4] = 1

            if "key.keyboard.w" in key_presses:
                label[5] = 1

            if "key.keyboard.1" in key_presses:
                label[6] = 1
                
            if "key.keyboard.2" in key_presses:
                label[7] = 1
                
            if "key.keyboard.3" in key_presses:
                label[8] = 1
                
            if "key.keyboard.4" in key_presses:
                label[9] = 1
                
            if "key.keyboard.5" in key_presses:
                label[10] = 1
                
            if "key.keyboard.6" in key_presses:
                label[11] = 1

            if "key.keyboard.7" in key_presses:
                label[12] = 1
                
            if "key.keyboard.8" in key_presses:
                label[13] = 1
                
            if "key.keyboard.9" in key_presses:
                label[14] = 1

            if "key.keyboard.e" in key_presses:
                label[15] = 1

            if "key.keyboard.space" in key_presses:
                label[16] = 1

            if "key.keyboard.a" in key_presses:
                label[17] = 1

            if "key.keyboard.d" in key_presses:
                label[18] = 1

            if "key.keyboard.left.shift" in key_presses or "key.keyboard.right.shift" in key_presses:
                label[19] = 1

            if "key.keyboard.left.control" in key_presses or "key.keyboard.right.control" in key_presses:
                label[20] = 1

            if 1 in mouse_presses:
                label[21] = 1

            labels.append(label)

    return labels

###### DOWNLOAD FILES ######

# Path to your JSON file
json_file_path = '../../data/Contractor_Index_Files/6xx_tree_chop.json'

# Directory to save the downloaded files
download_directory = '../../data/temp_training'

# Read the JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

basedir = data['basedir']

# Iterate through the links and download the files
for i in range(100):  # Assuming the links are stored in a list under the key 'links'
    # Get the file name from the link
    file_name = data['relpaths'][i].split('/')[-1]
    file_name_jsonl = data['relpaths'][i].split('/')[-1][:-3] + "jsonl"
    
    # Define the path to save the file
    file_path = os.path.join(download_directory, file_name)
    file_path_jsonl = os.path.join(download_directory, file_name_jsonl)
    
    # Download the mp4 file
    response = requests.get(basedir+data['relpaths'][i])
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f'Downloaded {file_name}')
    else:
        print(f'Failed to download {file_name}')

    # Download the jsonl file
    response = requests.get(basedir+data['relpaths'][i][:-3] + "jsonl")
    if response.status_code == 200:
        with open(file_path_jsonl, 'wb') as file:
            file.write(response.content)
        print(f'Downloaded {file_name_jsonl}')
    else:
        print(f'Failed to download {file_name_jsonl}')
        

###### FORMAT INPUT ######

files = os.listdir(download_directory)
videos_data = []

prepped_input_data = '../../data/temp_training/prepped_input_data.json'

for file in files:
    if file.endswith('.mp4'):
        video_path = os.path.join(download_directory, file)
        video_frames = process_video(video_path)
        videos_data.append(video_frames)

# Save the data to a JSON file
with open(prepped_input_data, 'w') as file:
    json.dump(videos_data, file)
    

##### FORMAT OUTPUT #####

files = os.listdir(download_directory)
labels_data = []

prepped_output_data = '../../data/temp_training/prepped_output_data.json'

for file in files:
    if file.endswith('.jsonl'):
        file_path = os.path.join(download_directory, file)
        labels = process_labels(file_path)
        labels_data.append(labels)

max_dx = 1
max_dy = 1

for i in range(len(labels_data)):
    for j in range(len(labels_data[i])):
        if abs(labels_data[i][j][2]) > max_dx:
            max_dx = abs(labels_data[i][j][2])

        if abs(labels_data[i][j][3]) > max_dy:
            max_dy = abs(labels_data[i][j][3])

for i in range(len(labels_data)):
    for j in range(len(labels_data[i])):
        labels_data[i][j][2] = labels_data[i][j][2]/max_dx
        labels_data[i][j][3] = labels_data[i][j][3]/max_dy

print(max_dx)
print(max_dy)

# Save the data to a JSON file
with open(prepped_output_data, 'w') as file:
    json.dump(labels_data, file)



