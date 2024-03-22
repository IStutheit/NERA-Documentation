import cv2
import numpy as np
import os

from concurrent.futures import ProcessPoolExecutor, as_completed


#------------------------------------------------------------
def process_single_video(video_path, output_dir=None):
    """
    Processes a single video file to extract and transform its frames into a list of normalized, 
    flattened grayscale images.

    Optionally saves all processed frames to a .npy file in the 
    specified output directory.

    Output file name will be the same as the input video file, 
    with "_proc.npy" appended in place of the original extension.

    Each frame is resized to 25x25 pixels, converted to grayscale, flattened into a vector, 
    and normalized so that pixel values are in the range [0, 1].

    Args:
        video_path (str): The path to the video file to be processed.
        output_dir (str, optional): The directory where processed frames will be saved as a .npy file. 
                                    If None, frames are not saved to disk.

    Returns:
        tuple: A tuple containing the video file name and a list of numpy.ndarray, each containing 
               the processed frames as 1D numpy arrays of normalized pixel values.
    """
    
    frames = []
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return video_path, []

    while True:
        ret, frame = cap.read() # Read the next frame

        if not ret: # If the frame is not read, we're at the end of the video, so break the loop
            break

        #Convert to grayscale, resize, and normalize the frame
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized_frame = cv2.resize(gray_frame, (25, 25)).flatten() / 255.0
        frames.append(resized_frame)

    cap.release() # Release the video capture object

    if output_dir:
        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        output_file_path = os.path.join(output_dir, f"{base_name}_proc.npy")
        np.save(output_file_path, np.array(frames))
        # STATUS MESSAGE
        print(f"Processed {len(frames)} frames from {video_path}.")

    return os.path.basename(video_path), frames
#------------------------------------------------------------


#------------------------------------------------------------
def process_video_frames(video_paths, output_dir=None, num_workers=None):
    """
    Processes multiple video files in parallel to extract and transform their frames.

    Args:
        video_paths (list of str): The paths to the video files to be processed.
        output_dir (str, optional): The directory where all processed frames will be saved as .npy files.
        num_workers (int, optional): The maximum number of worker processes to use. If None, the number 
                                     of workers is chosen automatically.

    Returns:
        dict: A dictionary where keys are video file names and values are lists of numpy.ndarray, 
              each containing the processed frames as 1D numpy arrays of normalized pixel values.
    """
    
    # STATUS MESSAGE
    print(f"\nProcessing {len(video_paths)} video files...")

    if num_workers is None:
        num_workers = os.cpu_count() or 4  # Fallback to 4 if os.cpu_count() returns None

    processed_videos = {}

    # Process each video file in parallel
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(process_single_video, video_path, output_dir): video_path for video_path in video_paths}
        for future in as_completed(futures):
            video_name, frames = future.result()
            processed_videos[video_name] = frames

    # STATUS MESSAGE
    print(f"Processed video data saved to {output_dir if output_dir else 'memory'}")

    return processed_videos
#------------------------------------------------------------




#------------------------------------------------------------
# EXAMPLE USAGE
#------------------------------------------------------------
if __name__ == "__main__":

    proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    video_dir_path = os.path.join(proj_root, 'data', 'temp_training')
    output_dir = os.path.join(proj_root, 'data', 'temp_training_processed')

    if os.path.exists(video_dir_path):
        video_files = [f for f in os.listdir(video_dir_path) if f.endswith(".mp4")]
        if video_files:
            video_paths = [os.path.join(video_dir_path, video_file) for video_file in video_files]
            processed_videos = process_video_frames(video_paths, output_dir)
            for video_name, frames in processed_videos.items():
                print(f"Processed {len(frames)} frames from {video_name}.")
        else:
            print(f"No .mp4 files found in {video_dir_path}")
#------------------------------------------------------------
