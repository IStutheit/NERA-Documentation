"""
**The driver class that combines all data downloading and processing classes**
"""
from .download_data_files import download_files
from .clear_training_data import clear_training_data
from .parse_urls_from_json import parse_urls_from_json
import os
from .video_processor import VideoProcessor
from .label_processor import LabelProcessor

def main():
    """
    Calls download_data_files, video_processor, and label_processor
    
    ---
    
    Utilizes the constants:
    
    >MINUTES_OF_FOOTAGE: The amount of footage to be downloaded (the length of each video file depends on which contractor dataset you are using. It is 1 minute for TreeChop)
    
    >WIDTH_HEIGHT: The size of the video file that will be compressed down to. (default as 25x25 pixels)
    
    """

    MINUTES_OF_FOOTAGE = 10
    WIDTH_HEIGHT = 64

    proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) #clear existing training data
    data_dir = os.path.join(proj_root, 'data')
    clear_training_data(data_dir)
    
    contractor_index_files = os.path.join(proj_root, 'data', 'Contractor_Index_Files') #download data
    json_file = os.path.join(contractor_index_files, '6xx_tree_chop.json')
    download_dir = os.path.join(proj_root, 'data', 'tree_chop_data')
    gameplay_data_dir = os.path.join(data_dir, 'tree_chop_data')


    urls = parse_urls_from_json(json_file)
    download_files(urls, download_dir, limit=MINUTES_OF_FOOTAGE*2) #must multiply by 2 to account for jsonl files which are paired with the mp4 files


    videoProcessor = VideoProcessor(WIDTH_HEIGHT) #process videos
    videoProcessor.process_all_videos(gameplay_data_dir)


    labelProcessor = LabelProcessor() #process labels
    labelProcessor.process_all_labels(gameplay_data_dir)

