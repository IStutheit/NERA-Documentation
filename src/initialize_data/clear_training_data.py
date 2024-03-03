import os

def clear_training_data(data_dir):
    """
    Deletes all files in the specified directory.
    Gotta be careful with this one!

    Args:
        data_dir (str): The path to the directory to be cleared.
    """
    # List all files in the folder
    files = os.listdir(data_dir)

    # Loop through the files and delete them
    for file in files:
        file_path = os.path.join(data_dir, file)
        if os.path.isfile(file_path):  # Check if it's a file
            os.remove(file_path)
            print(f'Deleted {file_path}')






#------------------------------------------------------------
# EXAMPLE USAGE
#------------------------------------------------------------
if __name__ == "__main__":
    clear_training_data()
    print("\nData cleared.\n")
