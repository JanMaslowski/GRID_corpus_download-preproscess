import os
import shutil
import pandas as pd


txt_file = 'gridcorpus/video/missing_faces.txt'
df = pd.read_csv(txt_file, sep=" ", header=None)
df.drop(labels=[0, 1, 2, 3], axis=1, inplace=True)
df.columns = ['path']
df['subfolder'] = df['path'].str.extract(r'(s\d+/[a-z0-9]+s)')
unique_subfolders = df['subfolder'].unique()

video_dir = 'gridcorpus/video'
broken_videos_dir = os.path.join(video_dir, 'broken_videos')
os.makedirs(broken_videos_dir, exist_ok=True)

for subfolder in unique_subfolders:
    if pd.notna(subfolder):  
        src_path = os.path.join(video_dir, subfolder)
        src_path_roi = os.path.join(video_dir, os.path.dirname(subfolder), f'ROI_{os.path.basename(subfolder)}')
        

        dst_path = os.path.join(broken_videos_dir, subfolder)
        dst_path_roi = os.path.join(broken_videos_dir, os.path.dirname(subfolder), f'ROI_{os.path.basename(subfolder)}')


        if os.path.exists(src_path):
            os.makedirs(os.path.dirname(dst_path), exist_ok=True) 
            shutil.move(src_path, dst_path)
            print(f"Moved {src_path} do {dst_path}")
        else:
            print(f"Directory {src_path} doesn't exist, skipping")

        if os.path.exists(src_path_roi):
            os.makedirs(os.path.dirname(dst_path_roi), exist_ok=True)
            shutil.move(src_path_roi, dst_path_roi)
            print(f"Moved {src_path_roi} do {dst_path_roi}")
        else:
            print(f"Directory {src_path_roi} doesn't exist, skipping")
