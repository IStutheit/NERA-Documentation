import os

def clear_training_data(data_dir):
    """
    Deletes all files in the specified directory.

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


#import config as cfg
# def clear_training_data():
#     """
#     Deletes all files in the specified directory.

#     Args:
#         data_dir (str): The path to the directory to be cleared.
#     """

#     data_dir = cfg.DATA_DIR + '/temp_training'
#     proc_data_dir = cfg.DATA_DIR + '/temp_training_processed'

#     # List all files in the folders
#     files = os.listdir(data_dir)
#     proc_files = os.listdir(proc_data_dir)

#     # Loop through the files and delete them
#     for file in files:
#         file_path = os.path.join(data_dir, file)
#         if os.path.isfile(file_path):  # Check if it's a file
#             os.remove(file_path)
#             print(f'Deleted {file_path}')

#     for file in proc_files:
#         file_path = os.path.join(proc_data_dir, file)
#         if os.path.isfile(file_path):
#             os.remove(file_path)
#             print(f'Deleted {file_path}')






#------------------------------------------------------------
# EXAMPLE USAGE
#------------------------------------------------------------
if __name__ == "__main__":
    clear_training_data()
    print("\nData cleared.\n")
