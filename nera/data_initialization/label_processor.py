import numpy as np
import os
import pickle
import random
import json

class LabelProcessor:
    def __init__(self):
        pass
    
    def process_labels(self, file_path):
        labels = []
        with open(file_path, 'r') as file:
            content = file.read()
            
        json_objects = content.split('\n')

        for json_str in json_objects:
            if json_str.strip():  # Skip empty lines
                label = [random.uniform(.1, 0.4) for i in range(22)] #Initializes labels to random values less than .5.
                data = json.loads(json_str)
                key_presses = data.get('keyboard', None).get('keys', None)
                mouse_presses = data.get('mouse', None).get('buttons',None)
                if json_objects.index(json_str) != 0:
                    data_prev = json.loads(json_objects[json_objects.index(json_str) - 1])
                    yaw_change = data.get('yaw', None) - data_prev.get('yaw', None)
                    pitch_change = data.get('pitch', None) - data_prev.get('pitch', None)

                    if abs(yaw_change) > 1:
                        yaw_change = yaw_change/abs(yaw_change)
                    elif abs(yaw_change) < .01:
                        yaw_change = random.uniform(.05, 0.4) - random.uniform(.05, 0.4)

                    if abs(pitch_change) > 1:
                        pitch_change = pitch_change/abs(pitch_change)
                    elif abs(pitch_change) < .01:
                        pitch_change = random.uniform(.05, 0.4) - random.uniform(.05, 0.4)
                else:
                    yaw_change = random.uniform(.05, 0.4) - random.uniform(.05, 0.4)
                    pitch_change = random.uniform(.05, 0.4) - random.uniform(.05, 0.4)

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

    def process_all_labels(self, labels_path):
        files = os.listdir(labels_path)
        labels_data = []

        prepped_output_data = labels_path+'/prepped_output_data.pkl'

        for file in files:
            if file.endswith('.jsonl'):
                file_path = os.path.join(labels_path, file)
                labels = self.process_labels(file_path)
                labels_data.append(labels)

        with open(prepped_output_data, 'wb') as file:
            pickle.dump(labels_data, file)
