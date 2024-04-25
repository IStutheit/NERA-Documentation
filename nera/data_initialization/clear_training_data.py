"""
**Deletes all files in the specified directory.**
"""

import os
import json

#from nera.utils.output_helpers import HORIZONTAL_LINE


def clear_training_data(data_dir):
    """
    ##Recursively search through the directory to delete all training data files.
    
    ---
    
    We use this to avoid using wildcards or other methods that could potentially delete files we don't want to delete.
    In every directory, and subdirectory, check for a "NERA_TERAINING_DATA_INDEX_FILE.json" file.

    ---
    
    ### Args:
    > data_dir (str): The directory to search for the "NERA_TERAINING_DATA_INDEX_FILE.json" files.
    
    ### Returns:
    > deleted_files (list of str): A list of all the files that were deleted.
    """
    # Store a list of all the files that were deleted
    deleted_files = []
    errors = []

    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file == "NERA_TRAINING_DATA_INDEX_FILE.json":
                with open(os.path.join(root, file), 'r') as f:
                    data = json.load(f)
                for file_path in data:
                    try:
                        os.remove(file_path)
                        deleted_files.append(file_path)
                    except FileNotFoundError:
                        errors.append(f"File not found: {file_path}")
                    except Exception as e:
                        errors.append(f"Error deleting file: {file_path}")
                        errors.append(e)

                # Delete the index file
                os.remove(os.path.join(root, file))

    #STATUS MESSAGE
    print("\n--------------------------------------------")
    print(f"Deleted {len(deleted_files)} files from {data_dir}")
    if errors:
        print(f"Errors:")
        for error in errors:
            print(error)
    for file in deleted_files:
        print(file)
    print("--------------------------------------------\n")






#------------------------------------------------------------
# EXAMPLE USAGE
#------------------------------------------------------------
if __name__ == "__main__":
    proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_dir = os.path.join(proj_root, 'data')
    clear_training_data(data_dir)
#------------------------------------------------------------

