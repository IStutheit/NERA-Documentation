import cv2
import numpy as np
import os


#------------------------------------------------------------
def process_video(video_path, output_dir=None):
    """
    Processes a video file to extract and transform its frames into a list of normalized, flattened grayscale images.

    Optionally saves all processed frames to a single .npy file in the specified output directory. Output file name will be the same as the input video file, with "_proc.npy" appended in place of the original extension.

    Each frame is resized to 25x25 pixels, converted to grayscale, flattened into a vector, and normalized so that
    pixel values are in the range [0, 1]. This preprocessing is useful for various computer vision and machine learning tasks.

    Args:
        video_path (str): The path to the video file to be processed.
        output_dir (str, optional): The directory where all processed frames will be saved as a single .npy file. If None, frames are not saved to disk.

    Returns:
        list of list of float: A list containing the processed frames as lists of normalized pixel values.
    """
    frames = []  # Initialize an empty list to store processed frames.
    
    # Ensure output directory exists if specified.
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # Attempt to open the video file.
        cap = cv2.VideoCapture(video_path)
        
        # Check if the video was successfully opened.
        if not cap.isOpened():
            print(f"Error opening video file: {video_path}")
            return frames  # Return the empty list if the video cannot be opened.

        while True:
            ret, frame = cap.read()  # Read the next frame from the video.
            if not ret:
                break  # Exit the loop if no frame is returned (end of video).

            # Perform resizing, grayscaling, flattening, and normalization.
            resized_frame = cv2.resize(frame, (25, 25))
            gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
            flattened_frame = gray_frame.flatten() / 255.0

            frames.append(flattened_frame.tolist())

    finally:
        cap.release()

    # If output directory is specified, construct the output filename based on the input video name.
    if output_dir:
        # Extract the base name of the video file (without extension) to use in the output file name.
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        output_file_path = os.path.join(output_dir, f"{base_name}_proc.npy")
        np.save(output_file_path, np.array(frames))
        print(f"All processed frames have been saved to {output_file_path}")

    return frames
#------------------------------------------------------------




#------------------------------------------------------------
# EXAMPLE USAGE
#------------------------------------------------------------
if __name__ == "__main__":
    # Example usage of the process_video function
    video_dir_path = "../data/temp_training/"

    # No output directory specified. Do not save processed frames.
    #check if the directory exists, and if there are any mp4 files in it
    # if os.path.exists(video_dir_path):
    #     video_files = [f for f in os.listdir(video_dir_path) if f.endswith(".mp4")]
    #     if len(video_files) > 0:
    #         video_path = os.path.join(video_dir_path, video_files[0])
    #         frames = process_video(video_path)
    #         print(f"Processed {len(frames)} frames from {video_path}")
    #     else:
    #         print(f"No .mp4 files found in {video_dir_path}")
    # else:
    #     print(f"Directory not found: {video_dir_path}")


    # Output directory specified. Save processed frames to disk.
    output_dir = "../data/temp_training_processed/"
    if os.path.exists(video_dir_path):
        video_files = [f for f in os.listdir(video_dir_path) if f.endswith(".mp4")]
        if len(video_files) > 0:
            video_path = os.path.join(video_dir_path, video_files[0])
            frames = process_video(video_path, output_dir)
            print(f"Processed {len(frames)} frames from {video_path}. Saved to {output_dir}")
        else:
            print(f"No .mp4 files found in {video_dir_path}")
    else:
        print(f"Directory not found: {video_dir_path}")
    


