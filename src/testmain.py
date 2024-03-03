import os
from initialize_data import download_files, parse_urls_from_json, process_video_frames, clear_training_data

def testModules():

    data_dir = '../data/'
    source_file = data_dir + 'Contractor_Index_Files/all_6xx_Jun_29.json'
    download_dir = data_dir + 'temp_training/'



    # Parse URLs from the JSON file
    urls = parse_urls_from_json(source_file)

    # Download files to the specified directory
    download_files(urls, download_dir)




    # Set the output directory for the processed frames
    output_dir = data_dir + 'temp_training_processed/'

    # Get a list of all .mp4 files in the download directory
    video_files = [f for f in os.listdir(download_dir) if f.endswith(".mp4")]

    video_file_paths = [os.path.join(download_dir, f) for f in video_files]

    # Process the video frames
    process_video_frames(video_file_paths, output_dir)


    print("\nData initialization complete.\n")


    

if __name__ == "__main__":
    testModules()