import os

folder_path = '../utils/temp_training'

# List all files in the folder
files = os.listdir(folder_path)

# Loop through the files and delete them
for file in files:
    file_path = os.path.join(folder_path, file)
    if os.path.isfile(file_path):  # Check if it's a file
        os.remove(file_path)
        print(f'Deleted {file_path}')
