import os
from initialize_data import download_files, parse_urls_from_json, process_video_frames, clear_training_data

def testModules():

    # We can just add an "initialize" function that takes in the source file,
    # download directory, processed frames directory, and number of workers as arguments.

    # I left it like this for now because we can more easily test the individual
    # components of the initialization process and change parameters for individual components as needed.


    # Set the source file and download directory
    data_dir = '../data/'
    source_file = data_dir + 'Contractor_Index_Files/all_6xx_Jun_29.json'
    download_dir = data_dir + 'temp_training/'

    # Parse URLs from the JSON file, and download them to the download directory
    urls = parse_urls_from_json(source_file)
    download_files(urls, download_dir)






    # Set the output directory for the processed frames
    processed_dir = data_dir + 'temp_training_processed/'

    # Get a list of all .mp4 files in the download directory
    video_files = [f for f in os.listdir(download_dir) if f.endswith(".mp4")]
    video_file_paths = [os.path.join(download_dir, f) for f in video_files]


    # There are two ways to process the video frames, I'm not totally sure which will be more useful for us.
    # If we have to read/write from disk, we should be using binary npy files, instead of writing to json and having to parse it again.
    # If we can avoid writing to disk altogether , we should just use the second method.

    # Process the video frames. This will return a dictionary of videos, where each video is a list of frames. It will also save the frames to the output directory.
    #videos = process_video_frames(video_file_paths, processed_dir)
    # Process the video frames WITHOUT WRITING TO DISK. This will return a dictionary of videos, where each video is a list of frames.
    videos = process_video_frames(video_file_paths)
    print("Number of videos: ", len(videos))

    # store the frames in a list for each video 
    #(each frame is a stored as a 1D numpy array of normalized pixel values)
    frames = [frame for video in videos.values() for frame in video]
    print("Number of frames: ", len(frames))


    print("\nData initialization complete.\n")


    

if __name__ == "__main__":
    testModules()