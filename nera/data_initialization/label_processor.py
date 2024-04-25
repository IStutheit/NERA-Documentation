from __future__ import annotations
import os
import json
import random
import pickle
#------------------------------------------------------------------------------
class LabelProcessor:

    #------------------------------------------------------------------------------
    def __init__(self):
        pass
    #------------------------------------------------------------------------------
    
    #------------------------------------------------------------------------------
    def read_jsonl_file(self, file_path: str) -> list:
        """
        ## Reads a JSONL file. Allows for multiple encodings to be tried.
        
        ---
        
        ### Arguments:
            > file_path (str): The path to the JSONL file.
        ### Returns:
            > list: A list of JSON objects.
        """
        encodings = ['utf-8', 'windows-1252']  # List common encodings to try
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    content = file.read().replace('\r\n', '\n')
                    return [json.loads(line) for line in content.splitlines() if line.strip()]
            except UnicodeDecodeError:
                # print the failure and inform the user which encoding will be tried next
                print(f"Encoding {encoding} failed for {file_path}; trying next encoding: {encodings[encodings.index(encoding) + 1]}")
                continue
            except Exception as e:
                print(f"Failed to read or parse {file_path} with {encoding}: {e}")
                return []
        print(f"All encodings failed for {file_path}. Check if the file is corrupted.")
        return []
    #------------------------------------------------------------------------------


    #------------------------------------------------------------------------------
    def process_label(self, data: dict, data_prev: dict = None) -> list:
        """
        ##Processes a single JSON entry to extract label information.

        ---

        ###Args:
            > data (dict): The JSON data to process.
            > data_prev (dict): The previous JSON data entry for calculating changes.
        ###Returns:
            > list: A list of label values.
        """
        label = [random.uniform(0.1, 0.4) for _ in range(22)]
        key_presses = data.get('keyboard', {}).get('keys', [])
        mouse_presses = data.get('mouse', {}).get('buttons', [])

        yaw_change = pitch_change = 0
        if data_prev:
            yaw_change = data.get('yaw', 0) - data_prev.get('yaw', 0)
            pitch_change = data.get('pitch', 0) - data_prev.get('pitch', 0)
            yaw_change = self.adjust_change(yaw_change)
            pitch_change = self.adjust_change(pitch_change)

        self.update_labels(label, key_presses, mouse_presses, yaw_change, pitch_change)
        return label
    #------------------------------------------------------------------------------


    #------------------------------------------------------------------------------
    def adjust_change(self, change: float) -> float:
        """
        ##Adjusts yaw or pitch changes based on thresholds.
        
        ---

        ##Argumentss:
            > change (float): The change in yaw or pitch.
        ##Returns:
            > float: The adjusted change.
        """
        if abs(change) > 1:
            return change / abs(change)
        elif abs(change) < 0.01:
            return random.uniform(0.05, 0.4) - random.uniform(0.05, 0.4)
        return change
    #------------------------------------------------------------------------------


    #------------------------------------------------------------------------------
    def update_labels(self, label: list, key_presses: list, mouse_presses: list, yaw_change: float, pitch_change: float) -> None:
        """
        ##Updates the label array based on input data.
        
        ---

        ### Arguments:
            > label (list): The label array to update.
            > key_presses (list): A list of key presses.
            > mouse_presses (list): A list of mouse button presses.
            > yaw_change (float): The change in yaw.
            > pitch_change (float): The change in pitch.
        ### Returns:
            - None
        """
        button_map = {"0": 0, "1": 21}
        key_map = {
            "key.keyboard.s": 1, "key.keyboard.q": 4, "key.keyboard.w": 5, 
            "key.keyboard.1": 6, "key.keyboard.2": 7, "key.keyboard.3": 8,
            "key.keyboard.4": 9, "key.keyboard.5": 10, "key.keyboard.6": 11,
            "key.keyboard.7": 12, "key.keyboard.8": 13, "key.keyboard.9": 14,
            "key.keyboard.e": 15, "key.keyboard.space": 16, "key.keyboard.a": 17,
            "key.keyboard.d": 18, "key.keyboard.left.shift": 19, "key.keyboard.right.shift": 19,
            "key.keyboard.left.control": 20, "key.keyboard.right.control": 20
        }

        for button, idx in button_map.items():
            if int(button) in mouse_presses:
                label[idx] = 1
        for key, idx in key_map.items():
            if key in key_presses:
                label[idx] = 1
        label[2] = yaw_change
        label[3] = pitch_change
    #------------------------------------------------------------------------------


    #------------------------------------------------------------------------------
    def process_labels(self, file_path: str) -> list:
        """
        ## Processes all labels in a given file.
        
        ---
        
        ### Args:
            > file_path (str): The path to the file containing the labels.
        ### Returns:
            > list: A list of labels.
        """
        json_objects = self.read_jsonl_file(file_path)
        labels = []
        for i, data in enumerate(json_objects):
            prev_data = json_objects[i - 1] if i > 0 else None
            label = self.process_label(data, prev_data)
            labels.append(label)
        return labels
    #------------------------------------------------------------------------------

    #------------------------------------------------------------------------------
    def process_all_labels(self, labels_path: str) -> None:
        """
        ##Processes all label files in a directory.
        
        ---
        
        ### Args:
            > labels_path (str): The path to the directory containing the label files.
        ### Returns:
            > None
        """
        files = os.listdir(labels_path)
        labels_data = []
        prepped_output_data = os.path.join(labels_path, 'prepped_output_data.pkl')

        for file in files:
            if file.endswith('.jsonl'):
                file_path = os.path.join(labels_path, file)
                labels = self.process_labels(file_path)
                labels_data.append(labels)

        with open(prepped_output_data, 'wb') as file:
            pickle.dump(labels_data, file)
    #------------------------------------------------------------------------------

#------------------------------------------------------------------------------