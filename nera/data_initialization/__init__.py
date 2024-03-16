
#import the main functions for the data initialization

# from .download_data_files import download_files
# from .parse_urls_from_json import parse_urls_from_json
# from .process_video_frames import process_video_frames

# def initialize(source_file, download_dir, num_workers=None):
#     """
#     Initializes the data by downloading files from the given source file and parsing the options data.

#     Args:
#     - source_file: Path to the source JSON file containing the URLs.
#     - download_dir: The directory to download the files to.
#     - num_workers: The number of worker threads to use for downloading files.
#     """

#     # Parse the URLs from the source file
#     urls = parse_urls_from_json(source_file)

#     # Download the files
#     download_files(urls, download_dir, num_workers)

#     # Process the video frames
#     process_video_frames(download_dir)

#     print("Data initialization complete.")

from .download_data_files import download_files
from .parse_urls_from_json import parse_urls_from_json
from .process_video_frames import process_video_frames
from .clear_training_data import clear_training_data