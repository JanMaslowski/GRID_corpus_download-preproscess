import os
import shutil
import ffmpeg as ffmpeg_lib


main_folder = 'gridcorpus_hd_small/video'


def remove_video_dir(path):
    video_dir_path = os.path.join(path, 'video')
    
    # Check if the 'video' directory exists
    if os.path.exists(video_dir_path) and os.path.isdir(video_dir_path):
        shutil.rmtree(video_dir_path)
        print(f'Removed "video" directory: {video_dir_path}')
    else:
        print(f'"video" directory does not exist at path: {path}')
# Iterate through all primary subfolders (s1, s2, etc.)
for subfolder in os.listdir(main_folder):
    subfolder_path = os.path.join(main_folder, subfolder)
    
    if os.path.isdir(subfolder_path):
        # Walk through the directory tree
        for root, _, files in os.walk(subfolder_path):
            for file in files:
                if file.endswith('.mpg'):
                    source_path = os.path.join(root, file)
                    destination_path = os.path.join(subfolder_path, file)

                    # Move the file to the main subfolder (s1, s2, etc.)
                    if source_path != destination_path:
                        shutil.move(source_path, destination_path)
                        print(f'Moved {source_path} to {destination_path}')

        # Remove empty subdirectories
        remove_video_dir(subfolder_path)

print("All .mpg files have been moved to their respective main subfolders.")


# Iterate through all directories
for subfolder in os.listdir(main_folder):
    subfolder_path = os.path.join(main_folder, subfolder)
    
    if os.path.isdir(subfolder_path):
        
        nested_folder_path = os.path.join(subfolder_path, subfolder)
        if os.path.isdir(nested_folder_path):
            for file in os.listdir(nested_folder_path):
                shutil.move(os.path.join(nested_folder_path, file), subfolder_path)
            os.rmdir(nested_folder_path)
        
        for file in os.listdir(subfolder_path):
            if file.endswith('.mpg'):
                video_path = os.path.join(subfolder_path, file)
                

                file_name = os.path.splitext(file)[0]
                output_folder = os.path.join(subfolder_path, file_name)

                if os.path.exists(output_folder):
                    print(f'Folder {output_folder} już istnieje, pomijam przetwarzanie {file}')
                    continue
                

                os.makedirs(output_folder, exist_ok=True)
                output_pattern = os.path.join(output_folder, 'frame_%03d.jpg')
                
                (
                    ffmpeg_lib
                    .input(video_path)
                    .output(output_pattern, **{'qscale:v': 1}) # qscale:v lower value indicates higher quality
                    .run()
                )

                print(f'Przetworzono plik: {file}, klatki zapisane w: {output_folder}')

