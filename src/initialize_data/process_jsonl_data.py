import os
import json
import numpy as np

#------------------------------------------------------------
def process_labels(file_path, max_dx=1, max_dy=1):
    """
    Processes label data from a .jsonl file, extracting certain actions like key presses and mouse movements,
    normalizes mouse movement data, and structures the data for machine learning or analysis tasks.

    The function also scales mouse movement data based on provided maximum values for x and y movements.

    Args:
        file_path (str): The path to the .jsonl file containing label data.
        max_dx (float): The maximum value for mouse dx to use for normalization.
        max_dy (float): The maximum value for mouse dy to use for normalization.

    Returns:
        list of list of float: A list containing the processed and normalized labels.
    """
    labels = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():  # Skip empty lines
                data = json.loads(line)
                label = process_label_data(data, max_dx, max_dy)
                labels.append(label)

    return labels
#------------------------------------------------------------


#------------------------------------------------------------
def process_label_data(data, max_dx, max_dy):
    """
    Processes a single line of label data to extract key presses, mouse presses, and mouse movements,
    and normalizes the mouse movement data.

    Args:
        data (dict): A dictionary containing label data for a single frame.
        max_dx (float): The maximum dx value for normalization.
        max_dy (float): The maximum dy value for normalization.

    Returns:
        list: A list representing the processed and normalized label for a single frame.
    """
    label = [0] * 22  # Initialize label with 22 zeros

    key_presses = data.get('keyboard', {}).get('keys', [])
    mouse_presses = data.get('mouse', {}).get('buttons', [])
    mouse_movex = data.get('mouse', {}).get('dx', 0) / max_dx
    mouse_movey = data.get('mouse', {}).get('dy', 0) / max_dy

    key_mapping = {
        "key.keyboard.s": 1,
        "key.keyboard.q": 4,
        "key.keyboard.w": 5,
        "key.keyboard.space": 16,
        "key.keyboard.a": 17,
        "key.keyboard.d": 18,
        # Add additional key mappings as necessary
    }

    for key, index in key_mapping.items():
        if key in key_presses:
            label[index] = 1

    if 0 in mouse_presses: label[0] = 1
    if 1 in mouse_presses: label[21] = 1

    label[2] = mouse_movex
    label[3] = mouse_movey

    return label
#------------------------------------------------------------





#------------------------------------------------------------
# EXAMPLE USAGE
#------------------------------------------------------------
if __name__ == "__main__":
    download_directory = '../../data/temp_training/'
    prepped_output_data = '../../data/temp_training/prepped_output_data.json'
    labels_data = []

    if os.path.exists(download_directory):
        files = [f for f in os.listdir(download_directory) if f.endswith('.jsonl')]
        if files:
            for file in files:
                file_path = os.path.join(download_directory, file)
                labels = process_labels(file_path)
                labels_data.extend(labels)

            # Optionally, calculate max_dx and max_dy here if dynamic calculation is desired

            with open(prepped_output_data, 'w') as file:
                json.dump(labels_data, file)
            print(f"Processed labels from {len(files)} files. Saved to {prepped_output_data}")
        else:
            print(f"No .jsonl files found in {download_directory}")
    else:
        print(f"Directory not found: {download_directory}")
