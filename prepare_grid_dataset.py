import os
import cv2
from detect_crop_faces import crop_face_with_margin  # Importing the previously defined function

# Path to the main folder
main_folder = 'gridcorpus/video'
missing_faces_log = os.path.join(main_folder, 'missing_faces.txt')

# Parameters for cropping
MARGIN_X = 10   # Horizontal margin around the face
MARGIN_Y = 40   # Vertical margin around the face
OFFSET_Y = -27  # Vertical offset to adjust cropping

# Open the missing faces log file
with open(missing_faces_log, 'w') as log_file:
    # Iterate through each subfolder (s1, s2, ..., s34)
    for subfolder in os.listdir(main_folder):
        subfolder_path = os.path.join(main_folder, subfolder)
        
        # Skip if it's not a directory
        if not os.path.isdir(subfolder_path):
            continue
        
        # For each directory inside the current subfolder (e.g., bbaf2n)
        for folder_name in os.listdir(subfolder_path):
            folder_path = os.path.join(subfolder_path, folder_name)
            
            # Only process if it is a directory containing frames (e.g., 'bbaf2n')
            if os.path.isdir(folder_path):
                
                # Define the path for the ROI folder for storing cropped faces
                roi_folder_name = f"ROI_{folder_name}"
                roi_folder_path = os.path.join(subfolder_path, roi_folder_name)
                
                # Ensure the ROI folder exists
                os.makedirs(roi_folder_path, exist_ok=True)
                
                # Iterate over all frame images in the current folder (e.g., 'frame_001.jpg')
                for file in os.listdir(folder_path):
                    if file.startswith('frame_') and file.endswith('.jpg'):
                        frame_path = os.path.join(folder_path, file)
                        
                        # Use the crop function to process the frame and save it in the ROI directory
                        cropped_face = crop_face_with_margin(
                            frame_path, margin_x=MARGIN_X, margin_y=MARGIN_Y, offset_y=OFFSET_Y
                        )
                        
                        # If a face was detected and cropped, save it in the ROI folder
                        if cropped_face is not None:
                            cropped_filename = os.path.join(roi_folder_path, file)
                            cv2.imwrite(cropped_filename, cropped_face)
                            print(f'Cropped face saved to {cropped_filename}')
                        else:
                            # Log the frame with no detected face
                            log_file.write(f"No face detected in {frame_path}\n")
                            print(f'No face detected in {frame_path}, skipping.')

print("All frames processed. Missing faces logged in missing_faces.txt.")


