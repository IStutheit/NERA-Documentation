import cv2
import numpy as np
import os
import pickle
import tensorflow as tf

class VideoProcessor:
    def __init__(self, frameSize):
        self.frameSize = frameSize

    def process_video(self, video_path):
        frames = []
        cap = cv2.VideoCapture(video_path)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Resize the frame
            resized_frame = cv2.resize(frame, (64, 64))
            
            # Convert to grayscale
            gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
            
            # Flatten the frame
            #flattened_frame = gray_frame.flatten()
            
            # Append the flattened frame to the list
            frames.append(gray_frame.tolist())
        
        cap.release()

        frames.pop()

        for i in range(len(frames)):
            for r in range(len(frames[i])):
                for c in range(len(frames[i][r])):
                    frames[i][r][c] = frames[i][r][c]/255


        frame_stack = np.stack(frames, axis=0)
        autoencoder = tf.keras.models.load_model('../autoencoder.h5')
        encoded_imgs = autoencoder.predict(frame_stack)
        #print(encoded_imgs[0].shape)
        return encoded_imgs


    def process_all_videos(self, videos_path):
        files = os.listdir(videos_path)
        videos_data = []
        prepped_input_data = videos_path+'/prepped_input_data.pkl'

        for file in files:
            if file.endswith('.mp4'):
                video_path = os.path.join(videos_path, file)
                video_frames = self.process_video(video_path)
                videos_data.append(video_frames)

        with open(prepped_input_data, 'wb') as file:
            pickle.dump(videos_data, file)
        
        
